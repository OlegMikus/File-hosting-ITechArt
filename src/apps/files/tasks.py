import os
import shutil
import time
from datetime import timedelta, datetime
from typing import List, Any, Dict

from src.apps.accounts.models import User
from src.apps.files.constants import FILE_STORAGE__TYPE__TEMP, CHUNKS__STORAGE_TIME__DAYS, ALLOWED_FORMATS
from src.apps.files.models import FilesStorage, File
from src.apps.files.utils import create_file, is_valid_format, is_valid_hash_md5, send_email

from src.etl.celery import celery_app


@celery_app.task
def task_build_file(user_id: str,
                    file_storage_id: str,
                    data: Dict[str, Any],
                    chunks_paths: List[str],
                    temp_chunks_storage: str) -> None:

    user = User.objects.get(id=user_id)
    file_storage = FilesStorage.objects.get(id=file_storage_id)
    hash_sum = data.get('hash_sum')
    user_storage_dir = os.path.join(file_storage.destination, str(user.id))
    os.makedirs(user_storage_dir, 0o777, exist_ok=True)
    file_path = os.path.join(user_storage_dir, data.get('filename'))
    with open(file_path, 'ab') as target_file:
        for path in chunks_paths:
            with open(path, 'rb') as stored_chunk_file:
                target_file.write(stored_chunk_file.read())
            os.unlink(path)
    os.rmdir(temp_chunks_storage)
    errors = []
    if File.objects.filter(hash=hash_sum, user=user, size=data.get('total_size'), name=data.get('filename')).first():
        errors.append('File already exist')
    if not is_valid_format(file_path):
        errors.append(f'Unsupported file format, use one from this: {ALLOWED_FORMATS}')
    if not is_valid_hash_md5(data.get('total_size'), hash_sum, file_path):
        errors.append('Invalid hash')
    if errors:
        os.remove(file_path)
        send_email(title='Errors during build', message=errors, recipients=[user.email])
        return None
    create_file(user, file_storage, data)


@celery_app.task
def task_remove_file(file_path: str) -> None:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None
    os.remove(file_path)


@celery_app.task
def task_remove_deleted_files() -> None:
    files = File.all_objects.filter(is_alive=False)
    for file in files:
        if not os.path.exists(file.absolute_path) or not os.path.isfile(file.absolute_path):
            continue
        shutil.rmtree(file.absolute_path)


@celery_app.task
def task_remove_expired_chunks() -> None:
    storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)
    users_dirs = os.listdir(storage.destination)

    for user_dir in users_dirs:
        absolute_user_dir_path = os.path.join(storage.destination, user_dir)
        for dir_with_chunks in os.listdir(absolute_user_dir_path):
            absolute_dir_with_chunks_path = os.path.join(absolute_user_dir_path, dir_with_chunks)
            file_updated_time = datetime.strptime(time.ctime(os.path.getmtime(absolute_dir_with_chunks_path)), "%c")

            if datetime.now() - file_updated_time > timedelta(days=CHUNKS__STORAGE_TIME__DAYS):
                shutil.rmtree(absolute_dir_with_chunks_path)
