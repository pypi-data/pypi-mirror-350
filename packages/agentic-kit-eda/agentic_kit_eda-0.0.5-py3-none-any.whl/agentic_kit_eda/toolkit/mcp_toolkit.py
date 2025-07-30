import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools

from .flat_toolkit import FlatToolkit


class McpToolkit(FlatToolkit):

    connection: dict

    def dump(self):
        print('----dump McpToolkit----')
        super().dump()

    @classmethod
    def create(cls, connection: dict, name: str, description: str, **kwargs):
        tk = asyncio.run(cls.acreate(connection=connection, name=name, description=description))
        return tk

    @classmethod
    async def acreate(cls, connection: dict, name: str, description: str, **kwargs):
        tk = cls(name=name, description=description, connection=connection)
        tools = await load_mcp_tools(session=None, connection=connection)
        for tool in tools:
            tk.add_tool(tool)
        return tk
