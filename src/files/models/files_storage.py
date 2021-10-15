from django.db import models

from src.base.models import BaseModel


class FilesStorage(BaseModel):
    STORAGE_CHOICES = [
        ('IS', 'INTERMEDIATE_STORAGE'),
        ('PS', 'PERMANENT_STORAGE')
    ]
    storage_type = models.CharField(max_length=32, choices=STORAGE_CHOICES, default='IS',)
    destination = models.CharField(max_length=32)
