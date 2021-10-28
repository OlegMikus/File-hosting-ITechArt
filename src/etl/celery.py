import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')

celery_app = Celery()

celery_app.config_from_object('src.config.celery_consts', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'remove-chunks-after-week-of-keeping': {
        'task': 'src.apps.files.tasks.rm_expired_chunks',
        'schedule': crontab(day_of_week='*', hour=4, minute=0),
    }
}
