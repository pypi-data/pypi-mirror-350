from pydantic import BaseModel


class CeleryConfig(BaseModel):
    name: str = 'celery_app'

    broker: str = 'redis://localhost:6379/0'

    result_backend: str = 'redis://localhost:6379/1'

    include: list[str] = []
