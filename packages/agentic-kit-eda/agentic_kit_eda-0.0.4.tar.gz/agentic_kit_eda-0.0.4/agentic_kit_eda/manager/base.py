from abc import ABC, abstractmethod
from typing import Union

from langchain_core.tools import BaseTool

from agentic_kit_eda.toolkit.base import ToolkitBase


class ToolkitManagerBase(ABC):
    """toolkit管理器"""

    @abstractmethod
    def register(self, toolkit: ToolkitBase) -> bool:
        """注册toolkit"""
        raise NotImplemented

    @abstractmethod
    def unregister(self, tk_name_or_obj: Union[str, ToolkitBase]) -> bool :
        """注销toolkit"""
        raise NotImplemented

    @abstractmethod
    def get_toolkit(self, toolkit_name) -> Union[ToolkitBase, None]:
        """获取toolkit"""
        raise NotImplemented

    @abstractmethod
    def get_tools(self) -> list[BaseTool]:
        """获取全部的tools"""
        raise NotImplemented

    @abstractmethod
    def get_tool(self, tool_name: str, toolkit_name: Union[str, None] = None) -> Union[BaseTool, None]:
        """获取某个tool"""
        raise NotImplemented
