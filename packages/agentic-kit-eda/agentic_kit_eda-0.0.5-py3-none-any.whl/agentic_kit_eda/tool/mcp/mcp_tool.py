import asyncio
from typing import Any

from langchain_core.tools import BaseTool, StructuredTool
from langchain_mcp_adapters.sessions import create_session
from pydantic import BaseModel


class McpTool(BaseTool, BaseModel):
    tool_def: StructuredTool

    connection: dict

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        return super()._run(*args, **kwargs)

    async def _arun(self, *args, **kwargs) -> Any:
        # print('############ run ')
        # print(args)
        # print(kwargs)
        # print(self.tool_def.name)
        # print(self.tool_def.args)

        tool_args = kwargs
        if not tool_args:
            if len(tool_args) != len(self.tool_def.args.keys()):
                return 'error'
            tool_args = dict(zip(self.tool_def.args.keys(), tool_args))
        # print(tool_args)

        async with create_session(self.connection) as tool_session:
            await tool_session.initialize()
            res = await tool_session.call_tool(self.tool_def.name, tool_args)
            result = [item.model_dump() for item in res.content]
            return result
