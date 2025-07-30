from typing import Annotated

from langchain_core.tools import InjectedToolCallId
from langchain_core.utils.pydantic import TypeBaseModel
from pydantic import BaseModel
from typing_extensions import Literal

from ..base import RpcToolDef


class ApiDefArgsScheme(BaseModel):
    tool_call_id: Annotated[str, InjectedToolCallId]
    '''定义ApiDef时必填'''


class ApiDef(RpcToolDef):
    """model class for api definition."""
    url: str

    method: Literal["get", "post", "put", "delete", "patch"] = "get"

    args_schema: TypeBaseModel = None
