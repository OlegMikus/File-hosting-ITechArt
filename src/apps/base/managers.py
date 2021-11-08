from django.db import models
from django.db.models import QuerySet


class SoftDeleteQuerySet(models.query.QuerySet):
    """
    QuerySet whose delete() does not delete items, but instead marks the rows as not alive
    """
    def delete(self) -> None:
        self.update(is_alive=False)

    def get_alive(self) -> QuerySet:
        return self.filter(is_alive=True)


class IsAliveObjectsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return SoftDeleteQuerySet(self.model).get_alive()


class AllObjectsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return SoftDeleteQuerySet(self.model)
