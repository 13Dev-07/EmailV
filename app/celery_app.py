"""
Celery Application Configuration
"""

from celery import Celery
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.update(
    task_routes={
        'app.tasks.validate_email_task': 'validations',
    },
    result_expires=3600,
)