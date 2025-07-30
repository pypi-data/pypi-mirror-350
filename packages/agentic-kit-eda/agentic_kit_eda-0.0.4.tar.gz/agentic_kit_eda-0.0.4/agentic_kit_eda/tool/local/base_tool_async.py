from abc import ABC
from typing import Any

from langchain_core.tools import BaseTool

"""
怎样写一个本地可以异步调用的tool

方式1:
    1. 定义一个类，继承BaseToolAsync
    2. 子类中给属性直接赋值
    例如:
        class AsyncCalculatorAddTool(BaseToolAsync):
            class CalculatorAddToolArgsScheme(AsyncToolArgsScheme):
                x: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型']
                y: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型']
            name: str = 'CalculatorAddTool'
            description: str = '这个工具是加法计算器，可以计算两个数值的和。'
            args_schema = CalculatorAddToolArgsScheme
            async_func: Callable = calculator_add
    
方式2:
    1. 调用make_tool创建一个tool
    例如：
        class CalculatorAddToolArgsScheme(AsyncToolArgsScheme):
            x: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型']
            y: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型']
        
        tool = BaseToolAsync.make_tool(
            name='CalculatorAddTool',
            description='这个工具是加法计算器，可以计算两个数值的和。',
            args_schema=CalculatorAddToolArgsScheme,
            async_func=calculator_add
        )
        
async_func要求：
1. 返回值格式，其中必须透传**kwargs，因为包含tool_call_id：
return {
        'type': 'tool',
        'artifact': f'x + y = {res}',
        'content': res,
        'status': 'success',
        **kwargs
    }
"""


class BaseToolAsync(BaseTool, ABC):
    """异步tool的基类"""

    is_async: bool = True

    name: str

    description: str

    args_schema: Any
    '''符合async_func的参数，一定要继承自AsyncToolArgsScheme, 传递tool_call_id需要'''

    async_func: Any
    '''可以通过celery调用的异步方法'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, *args, **kwargs) -> Any:
        # print('=====BaseToolAsync=======')
        # print(args)
        # print(kwargs)
        if self.is_async:
            self.async_func.apply_async(args=args, kwargs=kwargs, retry=True)
            return ''
        else:
            self.async_func(*args, **kwargs)

    @classmethod
    def make_tool(cls, name: str, description: str, args_schema: Any, async_func: Any):
        return cls(name=name, description=description, args_schema=args_schema, async_func=async_func)
