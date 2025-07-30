from abc import ABC, abstractmethod

from langchain_core.tools import BaseToolkit


class ToolkitBase(BaseToolkit, ABC):
    """toolset的管理结构"""

    name: str
    '''toolkit名字，在toolkit manager中唯一'''

    description: str
    '''toolkit工具集的描述，为supervisor或router使用'''

    @abstractmethod
    def add_tool(self, **kwargs):
        """增加tool"""
        raise NotImplemented

    @abstractmethod
    def remove_tool(self, **kwargs):
        """移除tool"""
        raise NotImplemented

    def dump(self):
        pass
