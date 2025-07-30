from typing import Union, Dict, Any

from agentic_kit_eda.infrastructure.rpc.session import Session
from agentic_kit_eda.tool.rpc.ws.schema import WsToolDef
from agentic_kit_eda.tool.rpc.ws.ws_tool import WebsocketTool
from .flat_toolkit import FlatToolkit
from ..tool.rpc.base import RpcTool


class WebsocketToolkit(FlatToolkit):
    """a single/separated connection represent a tool group"""

    session: Session = None
    '''关联的session，当session端掉后，移除这个toolkit'''

    def __init__(self, session: Session, **kwargs):
        super().__init__(session=session, **kwargs)

    def add_tool(self, tool: RpcTool):
        """增加tool"""
        tool.toolkit = self
        super().add_tool(tool)

    @property
    def session_id(self):
        return self.session.id

    def send_message(self, message: Union[bytes, str, Dict[str, Any]]):
        """通过session发送消息"""
        return self.session.send_message(message=message)

    def dump(self):
        print('----dump WebsocketToolkit----')
        print('session = %s' % self.session)
        super().dump()

    @classmethod
    def create(cls, tool_def_list: list[WsToolDef], name: str, description: str, session: Session, **kwargs):
        assert tool_def_list is not None
        assert len(tool_def_list) > 0

        tk = cls(name=name, description=description, session=session)
        for tool_def in tool_def_list:
            tool_def = WsToolDef(**tool_def)
            ws_tool = WebsocketTool.create(tool_def=tool_def)
            tk.add_tool(ws_tool)
        return tk
