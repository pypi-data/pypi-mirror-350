from typing import Dict, Union

from typing_extensions import Any

from .base import HttpTool, format_url
from .http_tool_async_celery import http_get_async, http_post_async, http_patch_async, http_put_async, \
    http_delete_async


class GetToolAsync(HttpTool):
    http_method_desc: str = '''这是一个发送GET请求访问互联网的工具。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送get请求需要的参数，这个字符串会解析成json对象，全部放在参数请求列表中。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: get请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs,
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@GetToolAsync 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        tool_call_id = kwargs.pop('tool_call_id')
        http_get_async.apply_async(args=(url, kwargs, tool_call_id))
        return tool_call_id


class PostToolAsync(HttpTool):
    http_method_desc: str = '''这是一个发送POST请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送post请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: post请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@PostToolAsync 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        tool_call_id = kwargs.pop('tool_call_id')
        http_post_async.apply_async(args=(url, kwargs, tool_call_id))

        print('to = %s' % tool_call_id)
        return tool_call_id


class PatchToolAsync(HttpTool):
    http_method_desc: str = '''这是一个发送PATCH请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送patch请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: patch请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@PatchToolAsync 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        tool_call_id = kwargs.pop('tool_call_id')
        http_patch_async.apply_async(args=(url, kwargs, tool_call_id))
        return tool_call_id


class PutToolAsync(HttpTool):
    http_method_desc: str = '''这是一个发送PUT请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送put请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: put请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@PutToolAsync 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        tool_call_id = kwargs.pop('tool_call_id')
        http_put_async.apply_async(args=(url, kwargs, tool_call_id))
        return tool_call_id


class DeleteToolAsync(HttpTool):
    http_method_desc: str = '''这是一个发送DELETE请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送delete请求需要的参数，这个字符串会解析成json对象，全部放在参数请求列表中。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: delete请求获取到的结果，text格式。'''

    def _run(
        self,
        **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@DeleteToolAsync 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        tool_call_id = kwargs.pop('tool_call_id')
        http_delete_async.apply_async(args=(url, kwargs, tool_call_id))
        return tool_call_id
