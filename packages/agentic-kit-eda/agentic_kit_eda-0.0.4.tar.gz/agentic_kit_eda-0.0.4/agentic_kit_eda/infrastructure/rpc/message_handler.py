from abc import ABC, abstractmethod
from typing import Any

from .message import RpcToolUnRegisterMessage, RpcToolRegisterMessage, RpcToolCallResponseMessage, \
    RpcClientRegisterMessage, RpcClientUnRegisterMessage, RpcMessageTypeEnum, RpcChatMessage

"""rpc message的handler"""

class RpcMessageHandlerBase(ABC):
    """RPC handler基类"""

    message_type: RpcMessageTypeEnum
    '''消息类型'''

    is_once: bool = False
    '''是否一次性监听，如果一次性监听，当调用handler后，就移除listener'''

    id: str = ''


class RpcToolCallResponseMessageHandler(RpcMessageHandlerBase, ABC):
    """RPC tool call handler基类"""
    message_type = RpcMessageTypeEnum.TOOL_CALL_RESPONSE

    is_once: bool = True
    '''tool call响应属于一次性监听'''

    def __init__(self, tool_call_id: str):
        self.id = tool_call_id

    @abstractmethod
    def on_tool_call_response(self, message: RpcToolCallResponseMessage, connection: Any = None, **kwargs):
        raise NotImplemented


class RpcClientRegisterHandler(RpcMessageHandlerBase, ABC):
    """RPC client注册监听基类"""
    message_type = RpcMessageTypeEnum.CLIENT_REGISTER

    @abstractmethod
    def on_client_register(self, message: RpcClientRegisterMessage, connection: Any = None, **kwargs):
        raise NotImplemented


class RpcClientUnRegisterHandler(RpcMessageHandlerBase, ABC):
    """RPC client注册监听基类"""
    message_type = RpcMessageTypeEnum.CLIENT_UNREGISTER

    @abstractmethod
    def on_client_unregister(self, message: RpcClientUnRegisterMessage, connection: Any = None, **kwargs):
        raise NotImplemented


class RpcToolRegisterHandler(RpcMessageHandlerBase, ABC):
    """RPC tool注册监听基类"""
    message_type = RpcMessageTypeEnum.TOOL_REGISTER

    @abstractmethod
    def on_tool_register(self, message: RpcToolRegisterMessage, connection: Any = None, **kwargs):
        raise NotImplemented


class RpcToolUnRegisterHandler(RpcMessageHandlerBase, ABC):
    """RPC tool注册监听基类"""
    message_type = RpcMessageTypeEnum.TOOL_UNREGISTER

    @abstractmethod
    def on_tool_unregister(self, message: RpcToolUnRegisterMessage, connection: Any = None, **kwargs):
        raise NotImplemented


class RpcChatMessageHandler(RpcMessageHandlerBase, ABC):
    """RPC chat 基类"""
    message_type = RpcMessageTypeEnum.CHAT

    @abstractmethod
    def on_chat(self, message: RpcChatMessage, connection: Any = None, **kwargs):
        raise NotImplemented


RPC_ONCE_MESSAGE_HANDLER_TYPE = [
    RpcMessageTypeEnum.TOOL_CALL_RESPONSE
]

# class RpcNotifyMessageHandlerBase(RpcMessageHandlerBase, ABC):
#     """RPC notify基类"""
#     message_type = RpcMessageTypeEnum.NOTIFY
#
#     @abstractmethod
#     def on_notify(self, message: RpcNotifyMessage, connection: Any = None, **kwargs):
#         raise NotImplemented
