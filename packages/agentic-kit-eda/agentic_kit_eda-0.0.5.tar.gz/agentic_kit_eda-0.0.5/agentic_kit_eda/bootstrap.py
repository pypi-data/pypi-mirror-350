from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver

from agentic_kit_eda.infrastructure.event_driven.ws.ws_message_handler_manager import WsMessageHandlerManager
from agentic_kit_eda.infrastructure.rpc.fastapi.ws_connection_manager import WsConnectionManager
from agentic_kit_eda.infrastructure.rpc.message import RpcMessageTypeEnum
from agentic_kit_eda.infrastructure.rpc.session_mananger import SessionManager
from agentic_kit_eda.manager.ws_toolkit_manager import WsToolkitManager


class AgenticKitEda:

    checkpointer: MemorySaver
    '''全局checkpointer'''

    session_manager: SessionManager
    '''处理ws连接，保存session信息，用来发送消息'''

    ws_toolkit_manager: WsToolkitManager
    '''mixin（SessionManager, ToolkitManager）全局的session管理和ws tool管理'''

    connection_manager: WsConnectionManager
    '''全局的ws连接管理器'''

    ws_message_handler_manager: WsMessageHandlerManager
    '''全局的ws消息管理器'''

    def __init__(self, checkpointer: BaseCheckpointSaver = None):
        if checkpointer is None:
            checkpointer = MemorySaver()

        self.checkpointer = checkpointer

        self.session_manager = SessionManager.create()

        self.ws_toolkit_manager = WsToolkitManager.create(session_manager=self.session_manager)

        self.connection_manager = WsConnectionManager.create()
        self.connection_manager.add_connection_listener(self.session_manager)
        self.connection_manager.add_connection_listener(self.ws_toolkit_manager)

        self.ws_message_handler_manager = WsMessageHandlerManager.create()
        self.ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.TOOL_REGISTER, self.ws_toolkit_manager)
        self.ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.TOOL_UNREGISTER, self.ws_toolkit_manager)

global_eda = AgenticKitEda()
