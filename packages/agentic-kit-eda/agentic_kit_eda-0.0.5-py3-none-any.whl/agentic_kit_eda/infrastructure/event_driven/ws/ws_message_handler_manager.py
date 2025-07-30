from typing import Union

from starlette.websockets import WebSocket

from agentic_kit_eda.infrastructure.rpc.message import RpcMessageFactory, RpcMessageTypeEnum, RpcMessageBase
from agentic_kit_eda.infrastructure.rpc.message_handler import RpcMessageHandlerBase, RPC_ONCE_MESSAGE_HANDLER_TYPE


class WsMessageHandlerManager:
    _handlers: dict[str, list[RpcMessageHandlerBase]]
    '''
    handler的map结构：
    {
        "message_type1": [],
        "message_type2": [],
        ...
    }
    '''

    _once_handlers: dict[str, RpcMessageHandlerBase]
    '''一次性监听的handlers，与_handlers不会重复'''

    def __init__(self):
        self._handlers = {}
        self._once_handlers = {}

    def add_message_handler(self, message_type: RpcMessageTypeEnum, handler: RpcMessageHandlerBase):
        """添加消息处理器"""
        if handler.is_once or message_type in RPC_ONCE_MESSAGE_HANDLER_TYPE:
            if handler.id not in self._once_handlers:
                self._once_handlers[handler.id] = handler
        else:
            message_type_handlers = self._handlers.get(message_type, None)
            if message_type_handlers is None:
                message_type_handlers = []
                self._handlers[message_type] = message_type_handlers
            if handler not in message_type_handlers:
                message_type_handlers.append(handler)
        self.dump()

    def remove_message_handler(self, message_type: RpcMessageTypeEnum, handler: RpcMessageHandlerBase):
        if handler.is_once:
            if handler.id in self._once_handlers:
                self._once_handlers.pop(handler.id)
        else:
            message_type_handlers = self._handlers.get(message_type, None)
            if message_type_handlers is not None:
                if handler in message_type_handlers:
                    return message_type_handlers.remove(handler)
        self.dump()

    def get_message_handlers(self, message_type: RpcMessageTypeEnum):
        if message_type in RPC_ONCE_MESSAGE_HANDLER_TYPE:
            return self._once_handlers
        else:
            message_type_handlers = self._handlers.get(message_type, None)
            return message_type_handlers

    def _call_handler(self, message: RpcMessageBase, handler: RpcMessageHandlerBase, websocket: WebSocket):
        """调用handler"""
        if message.type == RpcMessageTypeEnum.CLIENT_REGISTER:
            handler.on_client_register(message=message, connection=websocket)
        elif message.type == RpcMessageTypeEnum.CLIENT_UNREGISTER:
            handler.on_client_unregister(message=message, connection=websocket)
        elif message.type == RpcMessageTypeEnum.TOOL_REGISTER:
            handler.on_tool_register(message=message, connection=websocket)
        elif message.type == RpcMessageTypeEnum.TOOL_UNREGISTER:
            handler.on_tool_unregister(message=message, connection=websocket)
        elif message.type == RpcMessageTypeEnum.TOOL_CALL_RESPONSE:
            handler.on_tool_call_response(message=message, connection=websocket)
        elif message.type == RpcMessageTypeEnum.CHAT:
            handler.on_chat(message=message, connection=websocket)
        else:
            print(f'unknown msg.type:{message.type} in WsMessageHandlerManager._call_handler')

    async def handle_message(self, websocket: WebSocket, message: Union[str, dict]):
        print('============WsMessageHandlerManager.handle_message: %s' % message)
        # 这里可以添加复杂的消息处理逻辑
        try:
            if isinstance(message, bytes):
                print('WsMessageHandler.handle_message [binary] warning: %s' % message)
            elif isinstance(message, dict) or isinstance(message, str):
                message = RpcMessageFactory.create(message)
                if message:
                    # note: 如果消息没有标记sender，就默认设置为session_id
                    if not message.sender:
                        message.sender = websocket.uid

                    if message.type in RPC_ONCE_MESSAGE_HANDLER_TYPE:
                        _handlers = self.get_message_handlers(message_type=message.type)
                        _handler = _handlers.get(message.receiver, None)
                        if _handler:
                            self._call_handler(message=message, handler=_handler, websocket=websocket)
                            # note: 如果是一次性监听，就移除
                            if _handler.is_once:
                                self.remove_message_handler(message_type=message.type, handler=_handler)
                    else:
                        _handlers = self.get_message_handlers(message.type)
                        if _handlers:
                            for _handler in _handlers:
                                self._call_handler(message=message, handler=_handler, websocket=websocket)
        except Exception as e:
            # note: 防止session 因为逻辑错误断开
            print('WsMessageHandlerManager.handle_message error: %s' % e)
            print(message)
            return

    def dump(self):
        print('=======WsMessageHandlerManager.dump======')
        print(self._handlers)
        print(self._once_handlers)

    @classmethod
    def create(cls):
        manager = cls()
        return manager
