from typing import Dict, Union

from langchain_community.utilities.requests import JsonRequestsWrapper
from typing_extensions import Any

from .base import HttpTool, format_url


class GetTool(HttpTool):
    http_method_desc: str = '''这是一个发送GET请求访问互联网的工具。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送get请求需要的参数，这个字符串会解析成json对象，全部放在参数请求列表中。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: get请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs,
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@GetTool 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        return JsonRequestsWrapper().get(url, **{'params': kwargs})


class PostTool(HttpTool):
    http_method_desc: str = '''这是一个发送POST请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送post请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: post请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@PostTool 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        return JsonRequestsWrapper().post(url, data=kwargs)


class PatchTool(HttpTool):
    http_method_desc: str = '''这是一个发送PATCH请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送patch请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: patch请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        """Run the tool."""
        print('@@@@@@@@@PatchTool 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        return JsonRequestsWrapper().patch(url, data=kwargs)


class PutTool(HttpTool):
    http_method_desc: str = '''这是一个发送PUT请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送put请求需要的参数，这个字符串会解析成json对象，放在请求的data字段里。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: put请求获取到的结果，text格式。'''

    def _run(
        self, **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@PutTool 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        return JsonRequestsWrapper().put(url, data=kwargs)


class DeleteTool(HttpTool):
    http_method_desc: str = '''这是一个发送DELETE请求访问互联网的工具。。请忽略之前的API调用参数。'''

    http_request_desc: str = '''输入:输入应该是一个json格式的字符串，包含了发送delete请求需要的参数，这个字符串会解析成json对象，全部放在参数请求列表中。请注意，始终对json字符串中的字符串使用双引号。如果无参数，则输入一个\'\'\'{}\'\'\''''

    http_response_desc: str = '''输出: delete请求获取到的结果，text格式。'''

    def _run(
        self,
        **kwargs
    ) -> Union[str, Dict[str, Any]]:
        print('@@@@@@@@@DeleteTool 接受到调用参数：%s' % kwargs)
        url = format_url(self.tool_def.url, **kwargs)
        return JsonRequestsWrapper().delete(url, **{'params': kwargs})
