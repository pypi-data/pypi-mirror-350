"""Server module for managing MCP server connections and tool execution."""

import asyncio
import os
import shutil
import sys
from contextlib import AsyncExitStack
from typing import Any, Dict
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from pygeai.proxy.tool import MCPTool
from pygeai.proxy.config import ProxySettingsManager


class Server:
    """
    Manages MCP server connections and tool execution.

    :param sever_name: str - Name of the server
    :param config: Dict[str, Any] - Server configuration
    :param settings: ProxySettingsManager - Proxy settings manager
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
        self.stdio_context: Any | None = None
        self.session: ClientSession | None = None
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        self.publicpreffix: str | None = None

    async def initialize(self) -> None:
        """
        Initialize the server connection.

        :return: None
        :raises: ValueError - If the command is invalid
        :raises: RuntimeError - If server initialization fails
        :raises: ConnectionError - If connection to server fails
        """
        self.publicpreffix = self.config.get("publicpreffix")
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

    async def list_tools(self) -> list[MCPTool]:
        """
        List available tools from the server.

        :return: list[Tool] - List of available tools
        :raises: RuntimeError - If server is not initialized
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                for tool in item[1]:
                    tools.append(
                        MCPTool(self.name, tool.name, tool.description, self.publicpreffix, tool.inputSchema)
                    )

        return tools

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