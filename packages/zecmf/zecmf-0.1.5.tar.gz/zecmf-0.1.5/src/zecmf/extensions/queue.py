"""Queue extension module.

Sets up Celery for asynchronous task processing with Flask integration.
"""

from celery import Celery, Task
from flask import Flask

celery = Celery()


def init_app(app: Flask) -> None:
    """Initialize Celery with the Flask app."""
    # Get configuration from app config with defaults
    broker_url = app.config.get("CELERY_BROKER_URL", "memory://")
    result_backend = app.config.get("CELERY_RESULT_BACKEND", "cache")

    celery.conf.update(
        broker_url=broker_url,
        result_backend=result_backend,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        task_track_started=True,
        task_time_limit=1800,  # 30 minutes
        worker_max_tasks_per_child=100,
        broker_connection_retry_on_startup=True,
    )

    class ContextTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    # Set ContextTask as the default task base class
    celery.conf.update(task_default_queue="default")
    celery.conf.task_cls = ContextTask
