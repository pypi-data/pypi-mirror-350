import json
from enum import StrEnum
from typing import Literal, Union

from langchain_core.messages import ToolCall, ToolMessage
from pydantic import BaseModel


class RpcMessageTypeEnum(StrEnum):
    """message类型枚举"""

    '''双向'''
    CHAT = 'chat'

    '''remote发送过来'''
    CLIENT_REGISTER = 'client_register'
    CLIENT_UNREGISTER = 'client_unregister'
    TOOL_REGISTER = 'tool_register'
    TOOL_UNREGISTER = 'tool_unregister'
    TOOL_CALL_RESPONSE = 'tool_call_response'

    '''发送给remote'''
    CLIENT_REGISTER_OK = 'client_register_ok'
    CLIENT_REMOVED = 'client_removed'  # 主动移除
    SERVER_DIED = 'server_died'
    TOOL_CALL = 'tool_call'


MESSAGE_TYPES = [
    RpcMessageTypeEnum.CLIENT_REGISTER,
    RpcMessageTypeEnum.CLIENT_REGISTER_OK,
    RpcMessageTypeEnum.CLIENT_UNREGISTER,
    RpcMessageTypeEnum.CLIENT_REMOVED,
    RpcMessageTypeEnum.TOOL_REGISTER,
    RpcMessageTypeEnum.TOOL_UNREGISTER,
    RpcMessageTypeEnum.TOOL_CALL,
    RpcMessageTypeEnum.TOOL_CALL_RESPONSE,
    RpcMessageTypeEnum.CHAT,
    RpcMessageTypeEnum.SERVER_DIED,
]


class RpcMessageBase(BaseModel):

    sender: str = ''

    receiver: str = ''

    type: str = Literal[*MESSAGE_TYPES]

    def to_json(self):
        return self.model_dump_json(indent=None)

    def to_pretty_json(self):
        return self.model_dump_json(indent=2)

    def to_send_json(self):
        return self.model_dump()


class RpcClientRegisterMessage(RpcMessageBase):
    """client注册消息"""

    type: str = RpcMessageTypeEnum.CLIENT_REGISTER

    info: dict
    '''
    {
        "type": "client_register",
        "info": {
            "app_id": "要连接app的id",
            "uid": "name or uuid",
            "description": "描述，可为空"
        }
    }
    '''


class RpcClientRegisterOkMessage(RpcMessageBase):
    """client注册成功通知消息"""

    type: str = RpcMessageTypeEnum.CLIENT_REGISTER_OK


class RpcClientRemovedMessage(RpcMessageBase):

    type: str = RpcMessageTypeEnum.CLIENT_REMOVED


class RpcServerDiedMessage(RpcMessageBase):
    """server app停止"""

    type: str = RpcMessageTypeEnum.SERVER_DIED


class RpcClientUnRegisterMessage(RpcMessageBase):
    """client主动取消注册, sender就是client_id"""

    type: str = RpcMessageTypeEnum.CLIENT_UNREGISTER


class RpcToolCallMessage(RpcMessageBase):
    """agent -> rpc，格式与langchain_core.messages.tool.ToolCall相同"""

    type: str = RpcMessageTypeEnum.TOOL_CALL

    tool_call: ToolCall

    direction: str
    '''RPC_TOOL_DIRECTION_ENUM'''


class RpcToolCallResponseMessage(RpcMessageBase):
    """rpc -> agent"""

    type: str = RpcMessageTypeEnum.TOOL_CALL_RESPONSE

    response: ToolMessage


class RpcToolRegisterMessage(RpcMessageBase):
    """rpc -> agent"""
    '''
    {
        "type": "tool_register",
        "toolkit_name": "calculator",
        "toolkit_description": "",
        "tools": [
            {
                "name": "add",
                "description": "add two numbers",
                "args": {
                    "x": {
                    },
                    "y": {
                    }
                },
                "direction": "bi-directional"
            },
            {
                "name": "print",
                "description": "print",
                "args": {
                    "message": "str"
                },
                "direction": "one-way"
            }
        ]
    }
    {"type":"tool_register","toolkit_name":"calculator","tool":[{"name":"add","description":"add two numbers","args":{"x":{},"y":{}},"direction":"one-way"}]}
    {"type":"tool_register","toolkit_name":"calculator","tool":[{"name":"add","description":"add two numbers","args":{"x":{},"y":{}},"direction":"one-way"},{"name":"echo","description":"echo","args":{"message":"str"},"direction":"bi-directional"}]}
    '''

    type: str = RpcMessageTypeEnum.TOOL_REGISTER

    toolkit_name: str

    toolkit_description: str

    tools: list[dict]


class RpcToolUnRegisterMessage(RpcMessageBase):
    """rpc -> agent"""
    '''
    {
        "type": "tool_unregister",
        "toolkit_name": "calculator"
    }
    {"type":"tool_unregister","toolkit_name":"calculator"}
    '''

    type: str = RpcMessageTypeEnum.TOOL_UNREGISTER

    toolkit_name: str


class RpcChatMessage(RpcMessageBase):
    """rpc -> agent"""

    type: str = RpcMessageTypeEnum.CHAT

    message: Union[str, dict]


class RpcMessageFactory:
    @classmethod
    def create(cls, message: Union[str, dict]) -> Union[RpcMessageBase, None]:
        if isinstance(message, str):
            message = json.loads(message)

        _type = message['type']
        if _type == RpcMessageTypeEnum.TOOL_UNREGISTER:
            return RpcToolUnRegisterMessage(**message)
        elif _type == RpcMessageTypeEnum.TOOL_REGISTER:
            return RpcToolRegisterMessage(**message)
        elif _type == RpcMessageTypeEnum.TOOL_CALL_RESPONSE:
            return RpcToolCallResponseMessage(**message)
        elif _type == RpcMessageTypeEnum.TOOL_CALL:
            return RpcToolCallMessage(**message)
        elif _type == RpcMessageTypeEnum.CHAT:
            return RpcChatMessage(**message)
        elif _type == RpcMessageTypeEnum.CLIENT_REGISTER:
            return RpcClientRegisterMessage(**message)
        elif _type == RpcMessageTypeEnum.CLIENT_REGISTER_OK:
            return RpcClientRegisterOkMessage(**message)
        elif _type == RpcMessageTypeEnum.CLIENT_UNREGISTER:
            return RpcClientUnRegisterMessage(**message)
        elif _type == RpcMessageTypeEnum.SERVER_DIED:
            return RpcServerDiedMessage(**message)
        elif _type == RpcMessageTypeEnum.CLIENT_REMOVED:
            return RpcClientRemovedMessage(**message)
        else:
            # raise Exception('unknown ws message type: %s' % _type)
            return None
