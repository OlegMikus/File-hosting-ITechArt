import hashlib
import os
from typing import Dict, Any, List, BinaryIO, Union

import magic

from src.apps.accounts.models import User
from src.apps.files.constants import ALLOWED_FORMATS
from src.apps.files.models import FilesStorage, File


def get_chunk_name(filename: str, chunk_number: int) -> str:
    return f'{filename}_part_{chunk_number}'


def is_valid_hash_md5(hash_sum: str, file_path: str) -> bool:
    md5 = hashlib.md5()
    if not file_path:
        return False

    with open(file_path, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            md5.update(chunk)
        return hash_sum == md5.hexdigest()


def create_file(user: User,
                storage: FilesStorage,
                user_storage_dir: str,
                data: Dict[str, Any]
                ) -> None:
    File.objects.create(user=user, storage=storage,
                        destination=user_storage_dir, name=data.get('filename'),
                        description=data.get('description'), type=data.get('extension'),
                        size=data.get('total_size'), hash=data.get('hash_sum'))


def is_upload_complete(chunks_paths: List[str]) -> bool:
    return all([os.path.exists(path) for path in chunks_paths])


def is_valid_format(file_path: str) -> bool:
    if not file_path:
        return False

    with open(file_path, 'r') as users_file:
        file = users_file.read(1024)
        file_type = magic.from_buffer(file, mime=True)
        return file_type in ALLOWED_FORMATS
