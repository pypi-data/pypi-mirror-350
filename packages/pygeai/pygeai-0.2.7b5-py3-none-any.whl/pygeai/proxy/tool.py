from typing import Any
import json


class MCPTool:
    """
    Represents a tool exposed by an MCP (Multi-Channel Proxy) server.

    :param server_name: str - Name of the server exposing the tool
    :param name: str - Name of the tool
    :param description: str - Description of the tool's functionality
    :param publicpreffix: str - Public prefix of the tool
    :param input_schema: dict[str, Any] - JSON schema defining the expected input for the tool
    :return: MCPTool - Instance of the MCPTool class
    :raises: ValueError - If any required parameter is invalid or missing
    """

    def __init__(
        self, server_name: str, name: str, description: str, publicpreffix: str, input_schema: dict[str, Any]
    ) -> None:
        self.server_name: str = server_name
        self.name: str = name
        self.description: str = description
        self.input_schema: dict[str, Any] = input_schema
        self.publicpreffix: str = publicpreffix

    def get_full_name(self) -> str:
        """Get the full name of the tool."""
        return f"{self.server_name}__{self.name}"

    def is_public(self) -> bool:
        """Check if the tool is public."""
        return self.publicpreffix is not None

    def get_public_name(self) -> str:
        """Get the public name of the tool."""
        return f"{self.publicpreffix}.{self.name if self.server_name in self.publicpreffix else self.get_full_name()}"

    def format_for_llm(self) -> str:
        """Format tool information for LLM.

        Returns:
            A formatted string describing the tool.
        """
        return json.dumps({
                'type': 'function',
                'function': {
                    'name': self.get_full_name(),
                    'description': self.description or '',
                    'parameters': self.input_schema
                }
            })
