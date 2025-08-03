from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def make_celery():
    celery = Celery(
        "playlifts",
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_reject_on_worker_lost=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        result_expires=3600,
        result_persistent=True,
        task_track_started=True,
        task_send_sent_event=True,
    )

    return celery


celery = make_celery()

try:
    import tasks
except ImportError as e:
    print(f"Warning: Could not import tasks: {e}")
