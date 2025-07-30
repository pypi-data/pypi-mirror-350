from typing import Any, Annotated

from langchain_core.tools import BaseTool, InjectedToolCallId
from pydantic import BaseModel

from .schema import RpcToolDef


class ApiDefArgsScheme(BaseModel):
    tool_call_id: Annotated[str, InjectedToolCallId]
    '''定义ApiDef时必填'''


class RpcTool(BaseTool, BaseModel):
    """model class for rpc tool definition."""

    tool_def: RpcToolDef

    toolkit: Any = None
    '''属于哪个toolkit'''

    def __init__(self, tool_def: RpcToolDef, **kwargs):
        super().__init__(tool_def=tool_def, name=tool_def.name, description=tool_def.description, direction=tool_def.direction, **kwargs)

    def dump(self):
        print('-----RpcTool dump-----')
        # print('tk = %s' % self.toolkit.name)
        print('name = %s' % self.name)
        print('description = %s' % self.description)
        print('args = %s' % self.args)
