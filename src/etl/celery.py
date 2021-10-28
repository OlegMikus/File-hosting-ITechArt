import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')

celery_app = Celery()

celery_app.config_from_object('src.config.celery_consts', namespace='CELERY')

celery_app.autodiscover_tasks()
