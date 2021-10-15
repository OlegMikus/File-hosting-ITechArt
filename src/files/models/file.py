from django.db import models

from src.accounts.models import User
from src.base.models import BaseModel
from src.files.models.files_storage import FilesStorage


class File(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    destination = models.ForeignKey(FilesStorage, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(max_length=10)
    size = models.BigIntegerField()
    hash = models.CharField(max_length=32)
