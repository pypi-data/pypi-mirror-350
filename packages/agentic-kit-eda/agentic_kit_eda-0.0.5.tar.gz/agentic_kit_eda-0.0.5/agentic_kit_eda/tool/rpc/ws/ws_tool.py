import copy
from typing import Any, Union, Dict, Annotated

from langchain_core.messages import ToolCall, ToolMessage
from langchain_core.tools import InjectedToolCallId

from agentic_kit_core.utils.converter import convert_dict_to_fields, create_nested_model
from agentic_kit_eda.infrastructure.rpc.message import RpcMessageFactory, RpcMessageTypeEnum
from .schema import WsToolDef
from ..base import RpcTool, ApiDefArgsScheme


class WebsocketTool(RpcTool):
    tool_def: WsToolDef

    def __init__(self, tool_def: WsToolDef, **kwargs):
        # note: 动态创建args_schema class
        fields = convert_dict_to_fields(copy.deepcopy(tool_def.args_schema))
        args_schema_cls = create_nested_model(model_name='WebsocketToolArgsSchema', fields=fields) if fields else ApiDefArgsScheme
        class InnerWebsocketToolArgsSchema(args_schema_cls):
            tool_call_id: Annotated[str, InjectedToolCallId]
        kwargs['args_schema'] = InnerWebsocketToolArgsSchema

        super().__init__(tool_def, **kwargs)

    @property
    def args(self) -> dict:
        return self.tool_def.args_schema

    @property
    def session_id(self):
        return self.toolkit.session_id

    @classmethod
    def create(cls, tool_def: WsToolDef):
        return cls(tool_def=tool_def)

    def write_message(self, message: Union[bytes, str, Dict[str, Any]]):
        """通过session发送消息"""
        return self.toolkit.send_message(message=message,)

    def _run(self, **kwargs) -> Any:
        """发送tool call消息"""
        # TODO: tool call持久化，并且等待返回
        print('WebsocketTool._run: %s' % kwargs)

        tool_call_id = kwargs.pop('tool_call_id')
        message = RpcMessageFactory.create({
            'type': RpcMessageTypeEnum.TOOL_CALL,
            'sender': tool_call_id,
            'receiver': self.session_id,
            'tool_call': ToolCall(name=self.name, args=kwargs, id=tool_call_id),
            'direction': self.tool_def.direction
        })

        self.write_message(message.to_send_json())

        return ToolMessage(content='', tool_call_id=tool_call_id)
