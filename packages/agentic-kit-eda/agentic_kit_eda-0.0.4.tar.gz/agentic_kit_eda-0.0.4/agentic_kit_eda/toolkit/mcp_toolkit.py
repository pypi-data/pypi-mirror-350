import asyncio

from langchain_mcp_adapters.sessions import Connection, create_session
from langchain_mcp_adapters.tools import load_mcp_tools

from .flat_toolkit import FlatToolkit
from ..tool.mcp.mcp_tool import McpTool


class McpToolkit(FlatToolkit):

    connection: dict

    def dump(self):
        print('----dump McpToolkit----')
        super().dump()

    @classmethod
    def create(cls, connection: Connection, name: str, description: str, **kwargs):
        tk = asyncio.run(cls.acreate(connection=connection, name=name, description=description))
        return tk

    @classmethod
    async def acreate(cls, connection: dict, name: str, description: str, **kwargs):
        tk = cls(name=name, description=description, connection=connection)
        async with create_session(connection) as session:
            print('MCP server session已建立')
            await session.initialize()
            print('MCP server session已初始化')

            tools = await load_mcp_tools(session)
            for tool in tools:
                tk.add_tool(McpTool(name=tool.name, description=tool.description, args=tool.args, tool_def=tool, connection=connection))
        return tk
