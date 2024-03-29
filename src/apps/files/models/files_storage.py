from django.db import models

from src.apps.base.models import BaseModel
from src.apps.files.constants import FILE_STORAGE__TYPE__TEMP, FILE_STORAGE__TYPE__PERMANENT


class FilesStorage(BaseModel):

    type = models.CharField(max_length=32, choices=(
        (FILE_STORAGE__TYPE__TEMP, 'Temporary Storage'),
        (FILE_STORAGE__TYPE__PERMANENT, 'Permanent Storage'),
    ))
    destination = models.CharField(max_length=128)

    class Meta:
        db_table = 'files_storage'
