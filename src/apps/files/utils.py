import hashlib
import os
from typing import Dict, Any, List

import magic

from src.apps.accounts.models import User
from src.apps.files.constants import ALLOWED_FORMATS
from src.apps.files.models import FilesStorage, File


def get_chunk_name(filename: str, chunk_number: int) -> str:
    return f'{filename}_part_{chunk_number}'


def calculate_hash_md5(file_path) -> str:
    md5 = hashlib.md5()

    chunk = 0
    while chunk != b'':
        chunk = file_path.read(1024)
        md5.update(chunk)
    return md5.hexdigest()


def create_file(user: User,
                storage: FilesStorage,
                file_path: str,
                data: Dict[str, Any]
                ) -> None:
    File.objects.create(user=user, storage=storage,
                        destination=file_path, name=data.get('filename'),
                        description=data.get('description'), type=data.get('extension'),
                        size=data.get('total_size'), hash=data.get('hash_sum'))


def is_upload_complete(chunks_paths: List[str]) -> bool:
    return all([os.path.exists(path) for path in chunks_paths])


def is_valid_format(file_path: str) -> bool:
    with open(file_path, 'r') as users_file:
        file = users_file.read(1024)
        file_type = magic.from_buffer(file, mime=True)
    return file_type in ALLOWED_FORMATS
