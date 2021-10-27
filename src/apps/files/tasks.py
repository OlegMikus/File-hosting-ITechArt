import os
from typing import List, Any, OrderedDict, Dict

from src.apps.accounts.models import User
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
