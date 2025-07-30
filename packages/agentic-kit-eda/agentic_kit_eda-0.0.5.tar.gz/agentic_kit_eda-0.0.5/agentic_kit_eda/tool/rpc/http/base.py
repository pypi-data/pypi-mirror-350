from pydantic import BaseModel

from .schema import ApiDef, ApiDefArgsScheme
from ..base import RpcTool


def format_url(url: str, **kwargs) -> str:
    """格式化路径"""
    # note: 去除空格
    url = url.strip("\"'")

    # note: 将path参数填入url中，帮助llm填充params
    if url.find('{') and url.find('}'):
        url = url.format(url, **kwargs)

    return url


class HttpTool(RpcTool, BaseModel):
    """Base class for http requests tool."""

    """http_method_desc, http_request_desc, http_response_desc，子类赋值"""
    http_method_desc: str = ''
    http_request_desc: str = ''
    http_response_desc: str = ''

    description_fmt: str = """
    \t\thttp请求的url地址是：{url}
    \t\thttp请求的method是: {http_method_desc}
    \t\thttp请求的参数输入是: {http_request_desc}
    \t\thttp请求的返回输出是: {http_response_desc}
    \t\t业务功能描述：{description}
    """

    tool_def: ApiDef

    def __init__(self, tool_def: ApiDef, **kwargs):
        # note: 注入tool_call_id使用
        # assert tool_def.args_schema is not None
        kwargs['args_schema'] = tool_def.args_schema if tool_def.args_schema else ApiDefArgsScheme
        super().__init__(tool_def, **kwargs)

    @property
    def args(self) -> dict:
        return self.args_schema.model_json_schema()['properties'] if self.args_schema else {}

    @property
    def description(self) -> str:
        if self.tool_def:
            return self.description_fmt.format(**{
                'url': self.tool_def.url,
                'http_method_desc': self.http_method_desc,
                'http_request_desc': self.http_request_desc,
                'http_response_desc': self.http_response_desc,
                'description': self.tool_def.description,
            })
        else:
            return ''

    def dump(self):
        super().dump()
        print('url = %s' % self.tool_def.url)
        print('method = %s' % self.tool_def.method)
