import uuid

from django.db import models


class BaseModel(models.Model):
    """
    An abstract base class implementing a base fields for all models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_alive = models.BooleanField(default=True)

    class Meta:
        """
        Meta class
        """
        abstract = True
