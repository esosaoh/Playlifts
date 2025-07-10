from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def make_celery():
    celery = Celery(
        'listenup',
        broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    return celery

celery = make_celery()

# Import tasks after celery app is created to ensure proper registration
try:
    import tasks
except ImportError as e:
    print(f"Warning: Could not import tasks: {e}") 