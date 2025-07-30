import json
from typing import Union

import redis
import redis_lock

from .schema import RedisQueueConfig


class RedisHash:
    # name: str

    key_prefix: str

    redis_client: redis.Redis

    # 创建锁
    lock: redis_lock.Lock

    is_json: bool = True

    def __init__(self, key_prefix: str, config: RedisQueueConfig, is_json: bool = True):
        assert key_prefix is not None
        assert key_prefix != ''

        self.key_prefix = key_prefix
        self.redis_client = redis.Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            decode_responses=True
        )

        self.lock = redis_lock.Lock(self.redis_client, self.__class__.__name__)
        self.is_json = is_json

    def _get_key(self, key):
        return f"{self.key_prefix}{key}"

    def add(self, key: str, value: Union[str, dict]):
        name = self._get_key(key)

        if isinstance(value, dict):
            value = json.dumps(value)

        with self.lock:
            # note: nx=True, 不重复设置
            return self.redis_client.set(name=name, value=value, nx=True)

    def get(self, key: str):
        name = self._get_key(key)
        value = self.redis_client.get(name)

        if value:
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            if self.is_json:
                try:
                    json_value = json.loads(value)
                    return json_value
                except Exception as e:
                    return value
            else:
                return value
        else:
            return None

    def update(self, key: str, value: Union[str, dict]):
        name = self._get_key(key)

        if isinstance(value, dict):
            value = json.dumps(value)

        with self.lock:
            # note: xx=True, key存在时更新
            return self.redis_client.set(name=name, value=value, xx=True)

    def delete(self, key: str):
        name = self._get_key(key)
        with self.lock:
            if self.redis_client.exists(name):
                return self.redis_client.delete(name)  # 删除任务

    def clear(self):
        self.redis_client.flushdb()


# 测试 FIFO 队列
if __name__ == '__main__':
    queue = RedisHash(key_prefix='my_hash', config={
        'db': 10,
        'host': 'localhost',
        'port': 6379,
    })

    # 入队
    queue.add(key='1', value={'key1': 'value1'})
    v = queue.get(key='1')
    print(v)
    queue.add(key='1', value={'key1': 'value2'})
    v = queue.get(key='1')
    print(v)

    # queue.update('1', value={'key1': 'value2'})
    # v = queue.get(key='1')
    # print(v)
    #
    # queue.delete('1')
    # v = queue.get(key='1')
    # print(v)
    # queue.delete('1')
    # v = queue.get(key='1')
    # print(v)

    # queue.clear()
