import uuid
from typing import Any

from django.db import models

from src.apps.base.managers import IsAliveObjectsManager, AllObjectsManager


class BaseModel(models.Model):
    """
    An abstract base class implementing a base fields for all models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_alive = models.BooleanField(default=True)

    objects = IsAliveObjectsManager()
    all_objects = AllObjectsManager()

    def delete(self, *args: Any, **kwargs: Any) -> None:
        self.is_alive = False
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class
        """
        abstract = True
