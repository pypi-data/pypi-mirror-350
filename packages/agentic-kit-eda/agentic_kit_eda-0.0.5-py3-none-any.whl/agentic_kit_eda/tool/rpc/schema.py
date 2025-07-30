from enum import StrEnum
from typing import Literal, Union

from langchain_core.utils.pydantic import TypeBaseModel
from pydantic import BaseModel


class RPC_TOOL_DIRECTION_ENUM(StrEnum):
    ONE_WAY: str = 'one-way'
    BI_DIRECTIONAL: str = 'bi-directional'


class RpcToolDef(BaseModel):
    """model class for rpc tool definition."""
    name: str

    description: str

    direction: Literal[RPC_TOOL_DIRECTION_ENUM.ONE_WAY, RPC_TOOL_DIRECTION_ENUM.BI_DIRECTIONAL] = RPC_TOOL_DIRECTION_ENUM.BI_DIRECTIONAL
    '''单/双向调用'''

    is_async: bool = True
    '''是否异步，默认异步'''

    args_schema: Union[TypeBaseModel, dict] = None
    '''
    TypeBaseModel给http tool使用，dict给ws tool使用
    1. http tool 需要继承ApiDefArgsScheme(BaseModel)，进行tool.invoke时自动注入tool_call_id
    2. ws tool在注册时，上传json格式的tool说明
    '''
