import asyncio
from abc import ABC, abstractmethod
from asyncio import Task
from typing import Union

from langchain_core.runnables.schema import StreamEvent

TERMINATE_CMD = 'InnerMessageQueueCmd:terminate'


class InnerMessageQueueListener(ABC):
    @abstractmethod
    def on_message(self, message: Union[bytes, str, dict, StreamEvent]):
        raise NotImplemented


class InnerMessageQueue:
    message_queue: asyncio.Queue

    queue_task: Task

    listener: InnerMessageQueueListener

    terminate_flag: str

    @classmethod
    def create(cls, listener: InnerMessageQueueListener, maxsize: int = 0, terminate_flag: str = TERMINATE_CMD):
        queue = cls(listener=listener, maxsize=maxsize, terminate_flag=terminate_flag)
        return queue

    def __init__(self, listener: InnerMessageQueueListener, maxsize: int = 0, terminate_flag: str = TERMINATE_CMD):
        self.listener = listener
        self.terminate_flag = terminate_flag
        self.message_queue = asyncio.Queue(maxsize=maxsize)
        self.queue_task = asyncio.create_task(self.notify_message())

    async def notify_message(self):
        """接受消息队列，调用connection实际去发送消息"""
        while True:
            message = await self.message_queue.get()

            # 退出控制命令
            if isinstance(message, str):
                if self.terminate_flag == message:
                    await self.terminate()
                    break

            if self.listener:
                self.listener.on_message(message=message)

    async def terminate(self):
        if self.queue_task:
            self.queue_task.cancel()

    async def put(self, message: Union[bytes, str, dict, StreamEvent]):
        """
        将一个消息放入指定的队列
        """
        return await self.message_queue.put(message)

    def put_nowait(self, message: Union[bytes, str, dict, StreamEvent]):
        """
        将一个消息放入指定的队列
        """
        return self.message_queue.put_nowait(message)


if __name__ == '__main__':
    async def test_inner_message_queue():
        import time
        class L(InnerMessageQueueListener):
            def on_message(self, message: Union[bytes, str, dict]):
                print(f'on_message: {message}')

        q = InnerMessageQueue.create(listener=L(), terminate_flag='xxx')
        await q.put('hhhhhhhhh')
        time.sleep(1)
        await q.put({'k': 'v'})
        time.sleep(1)
        await q.put(b'aaaaaaaa')
        time.sleep(1)

        # await q.put(TERMINATE_CMD)
        await q.put('xxx')

        await asyncio.gather(*[q.queue_task], return_exceptions=True)
        print('#######END#######')

    looper = asyncio.new_event_loop()
    looper.run_until_complete(test_inner_message_queue())
