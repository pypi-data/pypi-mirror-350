import json
from abc import ABC, abstractmethod
from typing import Union

from redis.client import PubSub, Redis, PubSubWorkerThread

from agentic_kit_eda.infrastructure.redis.schema import RedisSubscriberConfig


class RedisSubscriberHandler(ABC):
    """业务自己实现"""
    @abstractmethod
    def on_subscribed(self, data: str):
        raise NotImplemented


class RedisSubscriber:
    redis_client: Redis

    subscriber: PubSub

    worker_thread: PubSubWorkerThread = None

    handlers: dict[str, RedisSubscriberHandler]
    '''tool_call_id: RedisSubscriberHandler'''

    channel_name: str

    config: RedisSubscriberConfig

    def subscribe_handler(self, message):
        """
        监听redis pub消息
        message格式：
        {
            'type': 'message',
            'pattern': None,
            'channel': b'celery_app.tasks.dispatcher.channel',
            'data': b'{"tool_call_id": "1234", "data": {"a": "b"}}'
        }
        """
        if message['type'] == 'message':
            channel = message['channel'].decode()
            print(f'{channel} got message {message}')
            if channel == self.channel_name:
                data = json.loads(message['data'].decode())
                tool_call_id = data.get('tool_call_id', None) or data.get('id', None)
                if tool_call_id and tool_call_id in self.handlers:
                    self.handlers[tool_call_id].on_subscribed(data)
                    # note: 一次调用后就移除
                    self.handlers.pop(tool_call_id)

    def __init__(self, config: RedisSubscriberConfig):
        assert config is not None
        self.config = config
        self.channel_name = self.config.channel_name

        self.redis_client = Redis(
            host=config.host,
            port=config.port,
            db=config.db,
        )

        self.handlers = {}
        self.subscriber = self.redis_client.pubsub()
        # note: 开启订阅
        self.subscriber.subscribe(**{
            self.channel_name: self.subscribe_handler
        })

    def start(self, **kwargs):
        """开启订阅，在单独thread"""
        # note：只启动一次
        if self.worker_thread is None:
            self.worker_thread = self.subscriber.run_in_thread(daemon=True)

    def stop(self, **kwargs):
        self.subscriber.unsubscribe(self.handlers.keys())
        self.worker_thread.stop()

    def add_handler(self, channel_name: str, handler: RedisSubscriberHandler):
        """动态增加handler"""
        assert  channel_name is not None
        assert  handler is not None
        if channel_name not in self.handlers:
            self.handlers[channel_name] = handler

    def publish(self, message: Union[str, dict]):
        if isinstance(message, dict):
            message = json.dumps(message)
        return self.redis_client.publish(self.channel_name, message)

    @classmethod
    def create(
        cls,
        config: RedisSubscriberConfig,
        auto_start: bool = True
    ):
        subscriber = RedisSubscriber(config=config)
        if auto_start:
            subscriber.start()
        return subscriber


# if __name__ == '__main__':
#     class CeleryTaskSubscriberMessageHandlerFake(RedisSubscriberHandler):
#         def on_subscribed(self, data: dict):
#             print('CeleryTaskSubscriberMessageHandlerFake: %s' % data)
#
#     class CeleryTaskSubscriberMessageHandlerFake2(RedisSubscriberHandler):
#         def on_subscribed(self, data: dict):
#             print('CeleryTaskSubscriberMessageHandlerFake2: %s' % data)
#
#     config = RedisSubscriberConfig(host='localhost', port=6379, db=15, channel_name="celery_app.tasks.dispatcher.channel")
#     s = RedisSubscriber.create(config=config, handler=CeleryTaskSubscriberMessageHandlerFake())
#     print("Main thread is running...%s" % threading.current_thread().ident)
#     s.start()
#
#     s.add_handler('celery_app.tasks.dispatcher.channel2', CeleryTaskSubscriberMessageHandlerFake2())
#
#     import time
#     time.sleep(2)  # 主线程运行一段时间
#
#     def pub():
#         print('###### pub thread: %s' % threading.current_thread().ident)
#         r = Redis(
#             host=config.host,
#             port=config.port,
#             db=config.db,
#         )
#         r.publish(config.channel_name, json.dumps({'thread_id': '1234', 'data': {'a': 'b'}}))
#         time.sleep(1)
#         r.publish('celery_app.tasks.dispatcher.channel2', json.dumps({'thread_id': '22222', 'data': {'a': 'b'}}))
#         time.sleep(1)
#         r.publish(config.channel_name, json.dumps({'thread_id': '1234', 'data': {'a': 'b'}}))
#
#     t = threading.Thread(target=pub, daemon=True)
#     t.start()
#
#     time.sleep(10)
#
#     # 停止后台线程
#     s.stop()
#     print("Main thread stopped.")
