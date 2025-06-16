# src/core/celery/app.py
from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "jpay_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.beat_schedule = {
    'monitor-transactions-every-30-seconds': {
        'task': 'src.core.celery.tasks.transaction_monitor.monitor_pending_transactions',
        'schedule': 30.0,  # every 30 seconds
    },
}
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
import src.core.celery.tasks.transaction_monitor
