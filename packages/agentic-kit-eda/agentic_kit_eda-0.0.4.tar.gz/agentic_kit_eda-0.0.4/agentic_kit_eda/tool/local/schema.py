from typing import Annotated

from langchain_core.tools import InjectedToolCallId
from pydantic import BaseModel


class AsyncToolArgsScheme(BaseModel):
    tool_call_id: Annotated[str, InjectedToolCallId]
