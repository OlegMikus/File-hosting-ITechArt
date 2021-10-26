from __future__ import absolute_import

from celery import Celery

celery_app = Celery()

celery_app.config_from_object('src.etl.celery_consts', namespace='CELERY')

celery_app.autodiscover_tasks()
