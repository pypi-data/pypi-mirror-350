from pathlib import Path
from typing import Any

from fastmcp import Client, FastMCP
from fastmcp.client.transports import ClientTransport
from fastmcp.exceptions import ToolError
from fastmcp.utilities.mcp_config import MCPConfig
from mcp.types import TextContent
from pydantic import AnyUrl

ClientTransportType = (
    ClientTransport | FastMCP | MCPConfig | AnyUrl | Path | dict[str, Any] | str
)


class MCPClient:
    def __init__(self, config: ClientTransportType):
        self.config = config
        self.client = Client(config)

    async def list_tools(self) -> str:
        """
        List all tools available in the MCP server.
        """
        tools = await self.client.list_tools()
        descriptions = "Available tools:\n"
        for tool in tools:
            descriptions += f"## {tool.name}\n{tool.description}\nArguments:\n"
            properties = tool.inputSchema.get("properties", {})
            for arg, meta in properties.items():
                arg_type = meta.get("type", "")
                arg_desc = meta.get("description", "")
                descriptions += f"* {arg}: {arg_type}\n    {arg_desc}\n"
            descriptions += "\n"
        return descriptions

    async def call_tool(
        self,
        tool_name: str,
        inputs: dict[str, str],
    ) -> str:
        """
        Call a specific tool with the given inputs.
        """
        try:
            resp = await self.client.call_tool(tool_name, inputs)
        except ToolError as e:
            return f"Error: calling tool {tool_name} with the following arguments:\n{inputs}\n\nError:\n{str(e)}"

        if isinstance(resp[0], TextContent):
            return f"Tool call result:\nTool name: {tool_name}\nTool inputs: {inputs}\nTool response:\n{resp[0].text}"
        else:
            return f"The tool did not return a text response. But Conflux can only handle text responses. Please check the tool's response type.\n\n{resp}"
