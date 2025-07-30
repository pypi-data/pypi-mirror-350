from typing import List, Any

from agentic_kit_core.utils.prompt import check_prompt_required_filed
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolCall
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool

from agentic_kit_eda.infrastructure.event_driven.ws.ws_message_handler_manager import WsMessageHandlerManager
from agentic_kit_eda.infrastructure.rpc.message import RpcToolCallResponseMessage, RpcMessageTypeEnum
from agentic_kit_eda.infrastructure.rpc.message_handler import RpcToolCallResponseMessageHandler
from agentic_kit_eda.tool.rpc.base import RpcTool
from .tool_call_interrupt_graph import ToolCallInterruptGraph


class ToolCallWsInterruptGraph(ToolCallInterruptGraph, RpcToolCallResponseMessageHandler):
    """interruptible ws tool call"""

    def on_tool_call_response(self, message: RpcToolCallResponseMessage, connection: Any = None, **kwargs):
        """
        实现RpcToolCallResponseMessageHandler，向asyncio.Queue() 发送消息，通知graph的interrupt继续执行
        """
        print('###########ToolCallWsInterruptGraph on_tool_call_response: %s' % message.response)
        self._finish_breakpoint(tool_call_id=message.response.tool_call_id, tool_call_response=message.response)

    def _on_tool_call(self, selected_tool: BaseTool, tool_call: ToolCall, task: Any):
        # note: 如果是异步tool，就配置断点等
        if isinstance(selected_tool, RpcTool):
            # note：设置断点
            self._set_breakpoint(task=task, tool_call=tool_call)

            tool_call_id = tool_call['id']
            self.id = tool_call_id
            self.ws_message_handler_manager.add_message_handler(
                message_type=RpcMessageTypeEnum.TOOL_CALL_RESPONSE,
                handler=self
            )
            res = selected_tool.invoke(tool_call)
            return res

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List,
        prompt_template: ChatPromptTemplate,
        ws_message_handler_manager: WsMessageHandlerManager,
        **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)
        self.ws_message_handler_manager = ws_message_handler_manager

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', cls.default_prompt)
        ws_message_handler_manager = kwargs.get('ws_message_handler_manager', None)
        assert prompt is not None
        assert ws_message_handler_manager is not None
        assert check_prompt_required_filed(prompt=prompt, required_field=['{ex_info}', '{task}', '{tools}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )
        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)
        return agent
