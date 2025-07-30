"""Server module for managing MCP server connections and tool execution."""
import asyncio
import os
import shutil
import sys
import httpx
from types import SimpleNamespace
from uuid import uuid4
from contextlib import AsyncExitStack
from abc import ABC, abstractmethod
from typing import Any, Dict
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from pygeai.proxy.tool import ProxiedTool
from pygeai.proxy.config import ProxySettingsManager
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import AgentCard, SendMessageRequest, MessageSendParams, Message, Task, SendMessageSuccessResponse


class ToolServer(ABC):
    """
    Interface for tool servers like MCP and A2A.

    Subclasses must implement methods to initialize the server,
    list available tools, and execute a tool.
    """
   
    def __init__(self, sever_name: str, config: Dict[str, Any], settings: ProxySettingsManager):
        """
        Initialize the server.
        
        :param sever_name: str - Name of the server
        :param config: Dict[str, Any] - Server configuration
        :param settings: ProxySettingsManager - Proxy settings manager
        """
        self.config = config
        self.settings = settings
        self.name: str = sever_name
        self.public_preffix: str | None = None
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the server connection.

        :return: None
        :raises: ValueError - If the command is invalid
        :raises: RuntimeError - If server initialization fails
        :raises: ConnectionError - If connection to server fails
        """
        pass

    @abstractmethod
    async def list_tools(self) -> list[ProxiedTool]:
        """
        List available tools from the server.

        :return: list[Tool] - List of available tools
        :raises: RuntimeError - If server is not initialized
        """
        pass

    @abstractmethod
    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        """
        Execute a tool with retry mechanism.

        :param tool_name: str - Name of the tool to execute
        :param arguments: dict[str, Any] - Tool arguments
        :param retries: int - Number of retry attempts
        :param delay: float - Delay between retries in seconds
        :return: Any - Tool execution result
        :raises: RuntimeError - If server is not initialized
        :raises: ConnectionError - If connection to server fails
        :raises: ValueError - If tool execution fails
        """
        pass

class A2AServer(ToolServer):
    """
    Manages A2A server connections and tool execution.
    """
    def __init__(self, sever_name: str, config: Dict[str, Any], settings: ProxySettingsManager):
        super().__init__(sever_name, config, settings)
        self.client: A2AClient | None = None
        self.card_url: str = self.config["url"]
        self.agent_card: AgentCard | None = None

    async def initialize(self) -> None:
        """
        Initialize the A2A client from the agent card and convert agent skills into tools
        compatible with OpenAI function call format.
        """
        try:
            self.httpx_client = httpx.AsyncClient()
            resolver = A2ACardResolver(httpx_client=self.httpx_client, base_url=self.card_url)
            self.agent_card = await resolver.get_agent_card()
            self.client = A2AClient(httpx_client=self.httpx_client, agent_card=self.agent_card)

        except httpx.HTTPError as e:
            sys.stderr.write(f"HTTP error initializing A2A server {self.name}: {e}\n")
            raise ConnectionError(f"Failed to connect to A2A server: {e}") from e
        except ValueError as e:
            sys.stderr.write(f"Invalid configuration for A2A server {self.name}: {e}\n")
            raise ValueError(f"Invalid A2A server configuration: {e}") from e
        except RuntimeError as e:
            sys.stderr.write(f"Runtime error initializing A2A server {self.name}: {e}\n")
            raise RuntimeError(f"A2A server initialization failed: {e}") from e
        
    async def list_tools(self) -> list[ProxiedTool]:
        if not self.client:
            raise RuntimeError(f"Server {self.name} not initialized")
        input_schema = {
            "type": "object",
            "properties": {
                "input-text": {
                    "type": "string",
                    "description": "The input text to send to the agent for execution."
                }
            },
            "required": ["input-text"]
        }
        tools = []
        for skill in self.agent_card.skills:
            tools.append(ProxiedTool(self.name, skill.name, skill.description, self.public_preffix, input_schema))
        return tools

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        sys.stdout.write(f"Executing {tool_name}...\n")
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': arguments["input-text"]}
                ],
                'messageId': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            params=MessageSendParams(**send_message_payload)
        )

        response = await self.client.send_message(request)
        result = []
        if isinstance(response.root, SendMessageSuccessResponse):
            if isinstance(response.root.result, Message) or True:
                result = response.root.result.parts
            elif isinstance(response.root, Task):
                sys.stderr.write(f"Task response: {response.root.result}\n")
            else:
                sys.stderr.write(f"Unknown response type: {type(response.root)}\n")
                raise ValueError(f"Unknown response type: {type(response.root)}")
        
        return SimpleNamespace(content=result, isError=False)
class MCPServer(ToolServer):
    """
    Manages MCP server connections and tool execution.

    :param sever_name: str - Name of the server
    :param config: Dict[str, Any] - Server configuration
    :param settings: ProxySettingsManager - Proxy settings manager
    """
    def __init__(self, sever_name: str, config: Dict[str, Any], settings: ProxySettingsManager):
        super().__init__(sever_name, config, settings)
        self.stdio_context: Any | None = None
        self.session: ClientSession | None = None

    async def initialize(self) -> None:
        self.public_preffix = self.config.get("publicpreffix")
        transport = self.config.get("transport") or ("sse" if "uri" in self.config else "stdio")
        try:
            if transport == "stdio":
                command = (
                    shutil.which("npx")
                    if self.config["command"] == "npx"
                    else self.config["command"]
                )
                if command is None:
                    raise ValueError("The command must be una cadena válida")

                server_params = StdioServerParameters(
                    command=command,
                    args=self.config["args"],
                    env={**os.environ, **self.config["env"]}
                    if self.config.get("env")
                    else None,
                )
            
                stdio_transport = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                read, write = stdio_transport
            elif transport == "sse":
                uri = self.config.get("uri")
                if not uri:
                    raise ValueError("Missing 'uri' for sse transport")

                sse_transport = await self.exit_stack.enter_async_context(
                    sse_client(
                        url=self.config["uri"],
                        headers=self.config.get("headers")
                    )
                )
                read, write = sse_transport
            else:
                raise ValueError(f"Unsupported transport: {transport}")
            
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()
            self.session = session
        except (RuntimeError, ConnectionError, ValueError) as e:
            sys.stderr.write(f"Error initializing server {self.name}: {e}\n")
            raise

    async def list_tools(self) -> list[ProxiedTool]:
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                for tool in item[1]:
                    tools.append(
                        ProxiedTool(self.name, tool.name, tool.description, self.public_preffix, tool.inputSchema)
                    )

        return tools

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        attempt = 0
        while attempt < retries:
            try:
                sys.stdout.write(f"Executing {tool_name}...\n")
                result = await self.session.call_tool(tool_name, arguments)
                return result

            except (RuntimeError, ConnectionError, ValueError) as e:
                attempt += 1
                sys.stderr.write(
                    f"Error executing tool: {e}. Attempt {attempt} of {retries}.\n"
                )
                if attempt < retries:
                    sys.stderr.write(f"Retrying in {delay} seconds...\n")
                    await asyncio.sleep(delay)
                else:
                    sys.stderr.write("Max retries reached. Failing.\n")
                    raise