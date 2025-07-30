import asyncio
from typing import Any, Union, Dict

from .fastapi.ws_connection_manager import ConnectionListener
from .message import RpcMessageBase
from .session import Session


class SessionManager(ConnectionListener):
    _session_map: dict[str, Session] = {}

    message_queue = asyncio.Queue()

    @classmethod
    def create(cls):
        manager = cls()
        return manager

    def __init__(self):
        asyncio.create_task(self.message_sender())
        '''初始化ws发送的消息队列'''

    # TODO: 优化message type的判断
    async def message_sender(self):
        """接受消息队列，调用connection实际去发送消息"""
        while True:
            message = await self.message_queue.get()
            _session = self.get_session(session_id=message['receiver'])
            if _session:
                # note: 根据不同message类型，调用不同发送方法
                if isinstance(message, str):
                    await _session.connection.send_text(message)
                elif isinstance(message, bytes):
                    await _session.connection.send_bytes(message)
                elif isinstance(message, dict):
                    await _session.connection.send_json(message)
                elif isinstance(message, RpcMessageBase):
                    await _session.connection.send_json(message.to_send_json())
                else:
                    print(f'unknown message: {message}')

    def add_session(self, session: Session):
        """注册session"""
        if session and self._session_map.get(session.id, None) is None:
            self._session_map[session.id] = session

    def drop_session(self, session_id: str):
        """丢弃session"""
        if self._session_map.get(session_id, None) is not None:
            self._session_map.pop(session_id)

    def get_session(self, session_id):
        return self._session_map.get(session_id, None)

    def send_message(self, message: Union[bytes, str, Dict[str, Any]]):
        """发送消息，将消息发送到队列中，队列消费者进行实际msg发送"""
        self.message_queue.put_nowait(message)

    def dump(self):
        print('=====SessionManager=====')
        print(self._session_map)

    def on_connect(self, connection: Any):
        session = Session(
            connection=connection,
            id=connection.uid,
            connection_metadata={'id': connection.uid},
            session_manager=self
        )
        print('new session ---- %s' % session.id)
        self.add_session(session=session)
        self.dump()

    def on_disconnect(self, connection: Any):
        self.drop_session(session_id=connection.uid)
        self.dump()
