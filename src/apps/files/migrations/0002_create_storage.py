from django.db import migrations

from src.config.settings import BASE_DIR
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT, FILE_STORAGE__TYPE__TEMP


def load_data(apps, schema_editor):

    storage_base_dir = BASE_DIR / 'storage'
    temp_storage_dir = storage_base_dir / 'temporary_storage'
    permanent_storage_dir = storage_base_dir / 'permanent_storage'

    FilesStorage = apps.get_model('files', 'FilesStorage')

    FilesStorage(type=FILE_STORAGE__TYPE__TEMP, destination=temp_storage_dir).save()
    FilesStorage(type=FILE_STORAGE__TYPE__PERMANENT, destination=permanent_storage_dir).save()


class Migration(migrations.Migration):
    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
