from django.db import models

from src.apps.accounts.models import User
from src.apps.base.models import BaseModel
from src.apps.files.models.files_storage import FilesStorage


class File(BaseModel):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    storage = models.ForeignKey(FilesStorage, on_delete=models.DO_NOTHING)
    destination = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(max_length=10)
    size = models.BigIntegerField()
    hash = models.CharField(max_length=512)

    class Meta:
        db_table = 'file'

    @property
    def absolute_path(self) -> str:
        return f'{self.storage.destination}/{self.destination}'
