from typing import Any

from agentic_kit_eda.infrastructure.rpc.fastapi.ws_connection_manager import ConnectionListener
from agentic_kit_eda.infrastructure.rpc.message import RpcToolRegisterMessage, RpcToolUnRegisterMessage
from agentic_kit_eda.infrastructure.rpc.message_handler import RpcToolRegisterHandler, RpcToolUnRegisterHandler
from agentic_kit_eda.infrastructure.rpc.session_mananger import SessionManager
from agentic_kit_eda.toolkit.ws_toolkit import WebsocketToolkit
from .flat_toolkit_manager import FlatToolkitManager


class WsToolkitManager(FlatToolkitManager, ConnectionListener, RpcToolRegisterHandler, RpcToolUnRegisterHandler):
    """websocket注册的toolkit管理"""

    session_manager: SessionManager

    @classmethod
    def create(cls, session_manager: SessionManager):
        manager = cls(session_manager=session_manager)
        return manager

    def __init__(self, session_manager: SessionManager):
        assert session_manager is not None
        self.session_manager = session_manager

    def dump(self):
        print('=====WsToolkitManager dump=====')
        for k, v in self.toolkit_map.items():
            print('-------')
            print(f'{k} -> {v}')

    """实现多个Handler"""

    def on_tool_register(self, message: RpcToolRegisterMessage, connection: Any = None, **kwargs):
        """注册tk"""
        print('============WsToolkitManager.on_register')
        _session_id = connection.uid
        _session = self.session_manager.get_session(session_id=_session_id)
        tk = WebsocketToolkit.create(
            tool_def_list=message.tools,
            name=message.toolkit_name,
            description=message.toolkit_description,
            session=_session
        )
        self.register(tk)
        self.dump()

    def on_tool_unregister(self, message: RpcToolUnRegisterMessage, connection: Any = None, **kwargs):
        """取消注册tk"""
        print('============WsToolkitManager.on_unregister')
        self.unregister(tk_name_or_obj=message.toolkit_name)
        self.dump()

    def on_connect(self, connection: Any):
        """忽略connect消息"""
        pass

    def on_disconnect(self, connection: Any):
        """处理disconnect消息，将关联的toolkit取消注册"""
        tk_list = []
        for toolkit in self.toolkit_map.values():
            if connection.uid == toolkit.session_id:
                tk_list.append(toolkit)

        if len(tk_list) > 0:
            for toolkit in tk_list:
                self.unregister(toolkit)
        self.dump()
