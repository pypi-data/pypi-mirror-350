import unittest

from agentic_kit_eda.tool.rpc.http import ApiDef
from agentic_kit_eda.tool.rpc.http.schema import ApiDefArgsScheme
from agentic_kit_eda.toolkit.http_toolkit import HttpToolkit


class MyTestCase(unittest.TestCase):
    def test_http_toolkit(self):

        class LLmChatInput(ApiDefArgsScheme):
            model_uid: str = Field(..., description="选择模型id，默认选择deepseek-chat^deepseek-chat^396@deepseek^18",
                                   title='选择模型id')
            q: str = Field(..., description="提问的问题描述", title='提问的问题描述')

        http_async = PostToolAsync(tool_def=ApiDef(url='http://221.229.0.177:9981/chat', method='post', name='llm_chat',
                                                   description='通过大模型调用来回答问题', is_async=True,
                                                   args_schema=LLmChatInput))


        api_list = [
            ApiDef(url='http://221.229.0.177:9981/v1/models', method='get', name='api1', description='d1', args=[
                {
                    "name": "name",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "title": "模型id",
                        "description": "模型id"
                    },
                    "description": "模型id"
                }
            ]),
            ApiDef(url='http://221.229.0.177:9981/chat', method='post', name='api2', description='d2', args={
                "properties": {
                    "model_uid": {
                        "type": "string",
                        "title": "选择模型ID",
                        "description": "选择模型ID"
                    },
                    "q": {
                        "type": "string",
                        "title": "提问",
                        "description": "提问",
                        "default": ""
                    },
                    "prompt": {
                        "type": "string",
                        "title": "提问",
                        "description": "提问",
                        "default": ""
                    },
                    "stream": {
                        "type": "boolean",
                        "title": "stream模式",
                        "description": "stream模式, true or false",
                        "default": False
                    },
                    "history": {
                        "items": {

                        },
                        "type": "array",
                        "title": "历史记录",
                        "description": "历史记录",
                        "default": []
                    },
                    "temperature": {
                        "type": "number",
                        "title": "temperature",
                        "description": "temperature，默认0.2",
                        "default": 0.2
                    },
                    "top_p": {
                        "type": "number",
                        "title": "top_p",
                        "description": "top_p",
                        "default": 0.8
                    }
                },
                "type": "object",
                "required": [
                    "model_uid"
                ],
                "title": "Body_chat_chat_post"
            }),
        ]

        tk = HttpToolkit.create(api_list=api_list, name='api tool', description='test api tool')
        tk.dump()

        # t1 = tk.get_tools()[0]
        # print('------')
        # print(t1.name)
        # res = t1.invoke({
        # })
        # print(res)
        # print(type(res))

        # t2 = tk.get_tools()[1]
        # print('------')
        # print(t2.name)
        # res = t2.invoke({
        #     'model_uid': 'deepseek-chat^deepseek-chat^396@deepseek^18',
        #     'q': '你好',
        # })
        # print(res)
        # print(type(res))


if __name__ == '__main__':
    unittest.main()
