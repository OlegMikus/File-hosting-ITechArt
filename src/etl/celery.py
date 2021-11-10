import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')

celery_app = Celery()

celery_app.config_from_object('src.config.celery_consts', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'remove_expired_chunks': {
        'task': 'src.apps.files.tasks.task.remove_expired_chunks',
        'schedule': crontab(day_of_week='*', hour=4, minute=0),
    },
    'remove_files_with_deleted_mark_once_per_month': {
        'task': 'src.apps.files.tasks.task_clean_storage',
        'schedule': crontab(month_of_year='*', day_of_month='1', hour=5, minute=0),
    }
}
