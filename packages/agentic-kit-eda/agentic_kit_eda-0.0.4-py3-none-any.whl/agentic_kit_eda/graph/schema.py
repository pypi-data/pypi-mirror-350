from operator import add
from typing import Annotated, Union

from langchain_core.messages import ToolMessage, AnyMessage

from agentic_kit_core.base.schema import BaseState, BaseStateInterrupt

class ToolCallState(BaseState):
    task: Union[str, list[str]]

    ex_info: str

    results: list[ToolMessage]

    call_log: list[AnyMessage]


class ToolCallWithBreakpointState(BaseStateInterrupt):
    task: Union[str, list[str]]

    ex_info: str

    results: Annotated[list[ToolMessage], add]

    call_log: Annotated[list[AnyMessage], add]
