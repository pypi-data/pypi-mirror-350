from typing import Union

from langchain_core.tools import BaseTool

from agentic_kit_eda.toolkit.flat_toolkit import FlatToolkit
from .base import ToolkitManagerBase


class FlatToolkitManager(ToolkitManagerBase):
    """flat结构的toolkit结构，一层管理"""

    toolkit_map: dict[str, FlatToolkit] = {}

    def register(self, toolkit: FlatToolkit) -> bool:
        assert toolkit is not None
        assert len(toolkit.get_tools()) > 0
        assert toolkit.name is not None and toolkit.name != ''

        if self.get_toolkit(toolkit.name) is None:
            self.toolkit_map[toolkit.name] = toolkit
            return True

        return False

    def unregister(self, tk_name_or_obj: Union[str, FlatToolkit]) -> bool :
        if isinstance(tk_name_or_obj, FlatToolkit):
            toolkit_name = tk_name_or_obj.name
        else:
            toolkit_name = tk_name_or_obj

        if self.get_toolkit(toolkit_name) is not None:
            self.toolkit_map.pop(toolkit_name)
            return True

        return False

    def get_toolkit(self, toolkit_name) -> Union[FlatToolkit, None]:
        return self.toolkit_map.get(toolkit_name, None)

    def get_tool(self, tool_name: str, toolkit_name: Union[str, None] = None) -> Union[BaseTool, None]:
        assert tool_name != ''

        if toolkit_name:
            tk = self.get_toolkit(toolkit_name)
            for tool in tk.get_tools():
                if tool.name == tool_name:
                    return tool
        else:
            for tk in self.toolkit_map.values():
                for tool in tk.get_tools():
                    if tool.name == tool_name:
                        return tool

        return None

    def get_tools(self) -> list[BaseTool]:
        tools = []
        for tk in self.toolkit_map.values():
            tools.extend(tk.get_tools())
        return tools
