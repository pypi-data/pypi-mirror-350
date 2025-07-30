from celery import Celery

from .schema import CeleryConfig


def create_celery_app(celery_config: CeleryConfig):
    def _create_app():
        _app = Celery(celery_config.name, broker=celery_config.broker, result_backend=celery_config.result_backend)
        _app.conf.update(
            result_backend=celery_config.result_backend,  # 用于存储任务结果
            accept_content=['json'],  # 接受的内容类型
            task_serializer='json',   # 任务序列化方式
            result_serializer='json', # 结果序列化方式
            timezone='UTC',           # 时区
            enable_utc=True,          # 使用 UTC 时间
            include=celery_config.include
        )
        return _app

    _app = _create_app()
    return _app
