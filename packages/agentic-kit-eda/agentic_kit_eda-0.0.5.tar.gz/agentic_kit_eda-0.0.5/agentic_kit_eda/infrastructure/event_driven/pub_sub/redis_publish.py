import functools
import json

from pydantic import BaseModel

from .redis_pubsub_manager import tool_call_publisher


def tool_call_publish_wrapper(publisher = tool_call_publisher):
    """
    装饰器：将函数的返回值发布到Redis的指定通道。
    :param publisher: Redis通道
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数
            result = func(*args, **kwargs)

            if isinstance(result, dict):
                result = json.dumps(result)
            elif isinstance(result, BaseModel):
                result = result.model_dump_json()
            elif isinstance(result, str):
                result = result
            else:  # 如果是对象，看是否支持序列化，如果不支持，就不publish
                try:
                    result = json.dumps(result)
                except TypeError:
                    pass

            # todo: result封装成ToolMessage
            if isinstance(result, str):
                publisher.publish(message=result)

            # 返回原始函数的结果
            return result

        return wrapper

    return decorator
