from langchain_core.tools import BaseTool
from pydantic import BaseModel

from .base import ToolkitBase


class FlatToolkit(ToolkitBase, BaseModel):
    """flat结构的tools结构，一层管理"""

    tools_map: dict[str, BaseTool] = {}
    '''map结构的tool管理'''

    def get_tools(self) -> list[BaseTool]:
        return list(self.tools_map.values())

    def add_tool(self, tool: BaseTool):
        """增加tool"""
        self.tools_map[tool.name] = tool

    def remove_tool(self, tool: BaseTool):
        """移除tool"""
        self.tools_map.pop(tool.name)

    def dump(self):
        for item in self.get_tools():
            item.dump()
