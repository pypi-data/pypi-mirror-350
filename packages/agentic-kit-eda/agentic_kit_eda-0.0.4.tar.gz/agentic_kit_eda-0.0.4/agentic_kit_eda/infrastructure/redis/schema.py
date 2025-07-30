from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str = 'localhost'

    port: int = '6379'

    db: int = 0


class RedisSubscriberConfig(RedisConfig):

    channel_name: str = ''
