from django.db import models

from src.accounts.models import User
from src.base.models import BaseModel


class File(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField()
    file = models.FileField(upload_to='file_storage/')

    def __str__(self) -> str:
        return f'File id in database: {self.id}'
