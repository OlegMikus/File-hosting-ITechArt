from django.db import models


class IsAliveObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_alive=True)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
