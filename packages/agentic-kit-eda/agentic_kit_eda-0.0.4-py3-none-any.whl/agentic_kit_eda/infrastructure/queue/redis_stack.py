import json
from typing import Union, Any

import redis

from .schema import RedisQueueConfig


class FifoStack:
    name: str

    redis_client: redis.Redis

    pubsub: None

    def __init__(self, name: str, config: RedisQueueConfig):
        assert name is not None

        self.name = name
        self.redis_client = redis.Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()

    def push(self, item: Union[str, dict]):
        """
        将元素插入队列尾部（入队）
        """
        if isinstance(item, dict):
            item = json.dumps(item)
        self.redis_client.rpush(self.name, item)

    def pop(self):
        """
        从队列头部移除元素（出队）
        """
        item = self.redis_client.lpop(self.name)
        if item:
            if isinstance(item, bytes):
                item = item.decode('utf-8')
            try:
                json_item = json.loads(item)
                return json_item
            except Exception as e:
                return item
        else:
            return None

    def size(self):
        """
        获取队列的长度
        """
        return self.redis_client.llen(self.name)

    def clear(self):
        """
        清空队列
        """
        self.redis_client.delete(self.name)

    def publish(self, message: Any):
        self.redis_client.publish(self.name, message)

    @property
    def listener(self):
        return self.pubsub


# 测试 FIFO 队列
if __name__ == '__main__':
    queue = FifoStack('my_fifo_queue', {
        'db': 9
    })

    # 入队
    queue.push({'key': 'value'})
    queue.push('你好2')
    queue.push('你好3')
    print("Queue size:", queue.size())

    # # 出队
    # print("Queue size:", queue.size())
    p = queue.pop()
    print(p)
    # print(type(p))
    # p = queue.pop()
    # print(type(p))
    # p = queue.pop()
    # print(type(p))

    # 清空队列
    # queue.clear()
