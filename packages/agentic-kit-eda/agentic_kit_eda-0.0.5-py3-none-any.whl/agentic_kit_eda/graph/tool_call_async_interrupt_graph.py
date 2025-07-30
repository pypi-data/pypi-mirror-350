import json
from typing import List, Any
from typing import Union

from agentic_kit_core.utils.prompt import check_prompt_required_filed
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolCall, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool, StructuredTool

from agentic_kit_eda.infrastructure.event_driven.pub_sub.redis_pubsub_manager import tool_call_subscriber
from agentic_kit_eda.infrastructure.event_driven.pub_sub.redis_subscriber import RedisSubscriberHandler
from agentic_kit_eda.tool.local.base_tool_async import BaseToolAsync
from agentic_kit_eda.tool.rpc.http.base import HttpTool
from .tool_call_interrupt_graph import ToolCallInterruptGraph


class ToolCallAsyncInterruptGraph(ToolCallInterruptGraph, RedisSubscriberHandler):
    """interruptible local&http tool call"""

    def on_subscribed(self, data: Union[str, dict]):
        """
        RedisSubscriberHandler，向asyncio.Queue() 发送消息，通知graph的interrupt继续执行
        """
        print('###### ToolCallAsyncInterruptGraph on_subscribed: %s' % data)
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, dict) and 'tool_call_id' in data:
            self._finish_breakpoint(tool_call_id=data.get('tool_call_id'), tool_call_response=ToolMessage(**data))

    def _on_tool_call(self, selected_tool: BaseTool, tool_call: ToolCall, task: Any):
        # note: 如果是异步tool，就配置断点等
        if ((isinstance(selected_tool, StructuredTool) and 'is_async' in selected_tool.metadata and selected_tool.metadata['is_async']) or
                (isinstance(selected_tool, HttpTool) and selected_tool.tool_def.is_async) or
                (isinstance(selected_tool, BaseToolAsync))):
            # note：设置断点
            self._set_breakpoint(task=task, tool_call=tool_call)

            # 添加回调监听
            tool_call_id = tool_call['id']
            tool_call_subscriber.add_handler(
                channel_name=tool_call_id,
                handler=self
            )

            # 调用tool
            res = selected_tool.invoke(tool_call)
            return res

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List,
        prompt_template: ChatPromptTemplate,
        **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', cls.default_prompt)
        assert prompt is not None
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
