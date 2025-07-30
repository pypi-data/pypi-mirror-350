from typing import Union

from agentic_kit_eda.infrastructure.redis.schema import RedisSubscriberConfig
from .redis_subscriber import RedisSubscriber


class RedisPubSubManager:
    channels: dict[str, RedisSubscriber]
    '''channel_name: subscriber'''

    def __init__(self):
        self.channels = {}

    def add_subscriber(self, channel_name: str, subscriber: RedisSubscriber, auto_start=False):
        if channel_name not in self.channels:
            self.channels[channel_name] = subscriber
            if auto_start:
                subscriber.start()

    def remove_subscriber(self, channel_name: str):
        if channel_name in self.channels:
            subscriber = self.channels.pop(channel_name)
            subscriber.stop()
            return subscriber
        return None

    def get_subscriber(self, channel_name: str):
        return self.channels.get(channel_name, None)

    def publish(self, channel_name: str, message: Union[str, dict]):
        subscriber = self.get_subscriber(channel_name)
        if subscriber:
            return subscriber.publish(message)

    @classmethod
    def create(cls):
        manager = cls()
        return manager

global_pubsub_manager = RedisPubSubManager.create()

"""通过celery异步调用tool相关配置"""
tool_call_subscriber = RedisSubscriber.create(config=RedisSubscriberConfig(channel_name='celery_app.tool_call.channel'), auto_start=True)
tool_call_publisher = tool_call_subscriber

'''通过celery执行local/http tool的异步调用监听'''
global_pubsub_manager.add_subscriber('celery_app.tool_call.channel', tool_call_subscriber)

#
# if __name__ == '__main__':
#     class CeleryTaskSubscriberMessageHandlerFake(RedisSubscriberHandler):
#         def on_subscribed(self, data: dict):
#             print('CeleryTaskSubscriberMessageHandlerFake: %s' % data)
#
#     class CeleryTaskSubscriberMessageHandlerFake2(RedisSubscriberHandler):
#         def on_subscribed(self, data: dict):
#             print('CeleryTaskSubscriberMessageHandlerFake2: %s' % data)
#
#     config = PubSubConfig(host='localhost', port=6379, db=15)
#     manager = RedisPubSubManager.create(config)
#     subscriber = RedisSubscriber.create(config=RedisSubscriberConfig())
#     handler1 = CeleryTaskSubscriberMessageHandlerFake()
#     handler2 = CeleryTaskSubscriberMessageHandlerFake2()
#     subscriber.add_handler('celery_app.tasks.dispatcher.channel1', handler1)
#     subscriber.add_handler('celery_app.tasks.dispatcher.channel2', handler2)
#     manager.add_subscriber('celery_app.tasks.dispatcher.channel', subscriber)
#     subscriber.start()
#     print("Main thread is running...%s" % threading.current_thread().ident)
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
#         manager.publisher.publish('celery_app.tasks.dispatcher.channel1', json.dumps({'thread_id': '1234', 'data': {'a': 'b'}}))
#         time.sleep(1)
#         manager.publisher.publish('celery_app.tasks.dispatcher.channel2', json.dumps({'thread_id': '22222', 'data': {'a': 'b'}}))
#         time.sleep(1)
#         manager.publisher.publish('celery_app.tasks.dispatcher.channel1', json.dumps({'thread_id': '12345555', 'data': {'a': 'b'}}))
#
#     t = threading.Thread(target=pub, daemon=True)
#     t.start()
#
#     time.sleep(10)
#
#     # # 停止后台线程
#     # s.stop()
#     print("Main thread stopped.")
