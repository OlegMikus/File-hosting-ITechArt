from django.db import models

from src.base.models import BaseModel


class FilesStorage(BaseModel):
    class Meta:
        db_table = 'files_storage'
    STORAGE_CHOICES = [
        ('temp', 'temp'),
        ('permanent', 'permanent')
    ]
    storage_type = models.CharField(max_length=32, choices=STORAGE_CHOICES)
    destination = models.CharField(max_length=32)
