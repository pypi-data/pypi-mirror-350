from contextlib import AsyncExitStack
from typing import Any, List, Dict, Tuple
import asyncio
import json
import sys
import requests
from urllib3.exceptions import MaxRetryError
import mcp.types as types
from pygeai.proxy.servers import Server, MCPTool
from pygeai.proxy.config import ProxySettingsManager
from pygeai.proxy.clients import ProxyClient, ToolProxyData, ToolProxyJobResult


class ServerManager:
    """
    Manages multiple MCP servers.

    :param servers_cfg: List[Dict[str, Any]] - List of server configurations
    :param settings: ProxySettingsManager - Proxy settings manager
    """

    def __init__(self, servers_cfg: List[Dict[str, Any]], settings: ProxySettingsManager):
        """
        Initialize the server manager.

        :param servers_cfg: List[Dict[str, Any]] - List of server configurations
        :param settings: ProxySettingsManager - Proxy settings manager
        """
        self.servers_cfg = servers_cfg
        self.settings = settings
        self.servers: Dict[str, Server] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    async def _initialize_servers(self) -> None:
        """
        Initialize all servers.

        :return: None
        :raises: Exception - If server initialization fails
        """
        for server_cfg in self.servers_cfg:
            sys.stdout.write(f"Initializing server {server_cfg['name']}\n")
            server = Server(server_cfg['name'], server_cfg, self.settings)
            try:
                await self.exit_stack.enter_async_context(server.exit_stack)
                await server.initialize()
                self.servers[server.name] = server
                sys.stdout.write(f"Server {server.name} initialized successfully\n")        
            except Exception as e:
                sys.stdout.write(f"Failed to initialize server {server.name}: {e}\n")
                raise

        for server in self.servers.values():
            sys.stdout.write(f"Listing tools for server {server.name}\n")
            tools = await server.list_tools()
            for tool in tools:
                self.tools[tool.get_full_name()] = tool
                sys.stdout.write(f"\tTool {tool.get_full_name()} added to server {server.name}\n")
    async def _initialize_client(self) -> ProxyClient:
        """
        Initialize the client.

        :return: ProxyClient - Initialized client instance
        :raises: ConnectionError - If connection fails
        :raises: MaxRetryError - If max retries are exceeded
        """
        try:
            alias = self.settings.get_current_alias()
            client = ProxyClient(self.settings.get_api_key(alias), self.settings.get_base_url(alias), self.settings.get_proxy_id(alias))
            sys.stdout.write(f"Registering proxy {self.settings.get_proxy_id(alias)} with name {self.settings.get_proxy_name(alias)} and description {self.settings.get_proxy_description(alias)} \n")
            client.register(proxy_data=ToolProxyData(
                id=self.settings.get_proxy_id(alias),
                name=self.settings.get_proxy_name(alias),
                description=self.settings.get_proxy_description(alias),
                affinity=self.settings.get_proxy_affinity(alias),
                tools=list(self.tools.values())
            ))
            sys.stdout.write(f"Proxy registered successfully\n")
            return client
        except (ConnectionError, MaxRetryError):
            raise
    
    async def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        """
        Execute a tool with retry mechanism.

        :param server_name: str - Name of the server to execute the tool on
        :param tool_name: str - Name of the tool to execute
        :param arguments: dict[str, Any] - Tool arguments
        :param retries: int - Number of retry attempts
        :param delay: float - Delay between retries in seconds
        :return: Any - Tool execution result
        :raises: RuntimeError - If server is not found or not initialized
        :raises: Exception - If tool execution fails after all retries
        """
        if server_name not in self.servers:
            raise RuntimeError(f"Server {server_name} not found")
        
        if tool_name not in self.tools:
            raise RuntimeError(f"Tool {tool_name} not found")
            
        server = self.servers[server_name]
        
        try:
            result = await server.execute_tool(self.tools[tool_name].name, arguments, retries, delay)
            return result
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            raise Exception(f"Failed to execute tool {tool_name} on server {server_name}: {e}") from e

    def extract_function_call_info(self, raw_json: str) -> Tuple[str, str]:
        """
        Extract function call info from raw JSON.

        :param raw_json: str - Raw JSON string
        :return: Tuple[str, str] - Tuple containing function name and arguments
        """
        try:
            data = json.loads(raw_json)
            return data['function']['name'], data['function']['arguments']
        except (json.JSONDecodeError, KeyError) as e:
            sys.stderr.write(f"Error extracting function call info: {e}\n")
            return None, None
        
    async def start(self) -> None:
        """
        Main proxy session handler.

        :return: None
        """
        retry_count = 0
        MAX_RETRIES = 10
        while retry_count < MAX_RETRIES:
            try:
                await self._initialize_servers()
                try:
                    client = await self._initialize_client()
                except (ConnectionError, TimeoutError, RuntimeError) as e:
                    sys.stdout.write(f"Error during client initialization: {e}\n")
                    for i in range(15, 0, -1):
                        sys.stdout.write(f"\rRetrying in {i} seconds...   ")
                        sys.stdout.flush()
                        await asyncio.sleep(1)
                    sys.stdout.write("\rRetrying now...           \n")
                    retry_count += 1
                    continue

                retry_count = 0
                sys.stdout.write(f"Waiting for jobs...\n")
                while True:
                    try:
                        jobs = client.dequeue()
                        retry_count = 0
                    except requests.exceptions.RequestException as e:
                        retry_count += 1
                        if retry_count >= MAX_RETRIES:
                            sys.stdout.write(f"Failed to dequeue jobs after {MAX_RETRIES} retries. \nException: {e}\nExiting...\n")
                            return
                        sys.stdout.write(f"Failed to dequeue jobs (attempt {retry_count}/{MAX_RETRIES}):\n")
                        for i in range(15, 0, -1):
                            sys.stdout.write(f"\rRetrying in {i} seconds...   ")
                            sys.stdout.flush()
                            await asyncio.sleep(1)
                        sys.stdout.write("\rRetrying now...           \n")
                        continue
                    for job in jobs:
                        sys.stdout.write(f"----------------------------------Job: {job.id}----------------------------------\n")
                        tool_name, arguments = self.extract_function_call_info(job.input)
                        if tool_name:
                            sys.stdout.write(f"Executing tool {job.server}/{tool_name} with arguments {arguments}\n")
                            try:
                                result = await self.execute_tool(job.server, tool_name, json.loads(arguments))
                            except (RuntimeError, ConnectionError, TimeoutError) as e:
                                sys.stdout.write(f"Error executing tool {tool_name}: {e}\n")
                                continue

                            if isinstance(result.content, list):
                                text_parts = []
                                for item in result.content:
                                    if isinstance(item, types.TextContent):
                                        text_parts.append(item.text)
                                    else:
                                        sys.stderr.write(f"Unknown content type {type(item)}\n")

                            if text_parts:
                                job.output = "\n".join(text_parts)
                                sys.stdout.write(f"result: {job.output} success: {not result.isError}\n")
                                try:
                                    client.send_result(ToolProxyJobResult(success=result.isError, job=job))
                                except (ConnectionError, TimeoutError, RuntimeError) as e:
                                    sys.stdout.write(f"Error sending result: {e}\n")
                            else:
                                sys.stdout.write(f"{result}\n")
                    await asyncio.sleep(1)
            finally:
                sys.stdout.write("Proxy stopped\n")
                await self.exit_stack.aclose()
