from django.db import models, migrations
from datetime import date

from src.files.constants import FILE_STORAGE__TYPE__PERMANENT, FILE_STORAGE__TYPE__TEMP


def load_data(apps, schema_editor):
    FilesStorage = apps.get_model('files', 'FilesStorage')

    FilesStorage(type=FILE_STORAGE__TYPE__TEMP,
                 destination='storage/temporary_storage/'
                 ).save()
    FilesStorage(type=FILE_STORAGE__TYPE__PERMANENT,
                 destination='storage/permanent_storage/'
                 ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
