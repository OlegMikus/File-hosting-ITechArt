import os
import shutil
import time
from datetime import timedelta, datetime
from typing import List, Any, Dict

from src.apps.accounts.models import User
from src.apps.files.constants import FILE_STORAGE__TYPE__TEMP
from src.apps.files.models import FilesStorage
from src.apps.files.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.apps.files.utils import create_file

from src.etl.celery import celery_app


@celery_app.task
def task_build_file(user_id: str,
                    file_storage_id: str,
                    data: Dict[str, Any],
                    chunks_paths: List[str],
                    file_path: str,
                    temp_chunks_storage: str) -> None:
    with open(file_path, 'ab') as target_file:
        for path in chunks_paths:
            with open(path, 'rb') as stored_chunk_file:
                target_file.write(stored_chunk_file.read())
            os.unlink(path)
    os.rmdir(temp_chunks_storage)
    user = User.objects.get(id=user_id)
    file_storage = FilesStorage.objects.get(id=file_storage_id)

    create_file(user, file_storage, file_path, data)


@celery_app.task
def remove_expired_chunks() -> None:
    storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)
    storage_destination = storage.destination
    users_dirs = os.walk(storage_destination)

    for directory in users_dirs:
        if len(list(directory[0].split('/'))) > 3:
            now = datetime.now()
            file_updated_time = datetime.strptime(time.ctime(os.path.getmtime(directory[0])), "%c")
            time_delta = timedelta(days=7)
            if now - file_updated_time > time_delta:
                shutil.rmtree(directory[0])
