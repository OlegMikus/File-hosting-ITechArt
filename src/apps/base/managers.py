from django.db import models
from django.db.models import QuerySet


class IsAliveObjectsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_alive=True)


class AllObjectsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().all()
