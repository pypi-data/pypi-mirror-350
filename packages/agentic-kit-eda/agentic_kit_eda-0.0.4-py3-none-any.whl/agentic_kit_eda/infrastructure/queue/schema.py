from pydantic import BaseModel


class RedisQueueConfig(BaseModel):
    host: str
    port: int
    db: int
