import uuid
from abc import ABC, abstractmethod
from typing import Any

from starlette.websockets import WebSocket


class ConnectionListener(ABC):
    """connect&disconnect监听"""

    @abstractmethod
    def on_connect(self, connection: Any):
        raise NotImplemented

    @abstractmethod
    def on_disconnect(self, connection: Any):
        raise NotImplemented


class WsConnectionManager:
    listeners: list[ConnectionListener]

    def __init__(self):
        self.listeners = []

    def add_connection_listener(self, listener: ConnectionListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_connection_listener(self, listener: ConnectionListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        uid = uuid.uuid4().hex
        websocket.session_id = uid
        websocket.uid = uid
        for listener in self.listeners:
            listener.on_connect(connection=websocket)

    def disconnect(self, websocket: WebSocket):
        print('lost connection ---- %s' % websocket.uid)
        for listener in self.listeners:
            listener.on_disconnect(connection=websocket)

    @classmethod
    def create(cls):
        manager = cls()
        return manager
