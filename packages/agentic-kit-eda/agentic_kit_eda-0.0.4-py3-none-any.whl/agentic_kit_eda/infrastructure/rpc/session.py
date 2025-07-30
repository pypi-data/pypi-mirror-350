from typing import Any, Union, Dict

from pydantic import BaseModel


class Session(BaseModel):
    """websocket session"""

    connection: Any
    '''rpc connection obj'''

    connection_metadata: dict
    '''connection metadata'''

    id: str
    '''uuid'''

    session_manager: Any = None

    def send_message(self, message: Union[bytes, str, Dict[str, Any]]):
        """通过connection发送消息"""
        if self.session_manager:
            self.session_manager.send_message(message=message)
