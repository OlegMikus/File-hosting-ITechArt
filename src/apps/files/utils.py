import hashlib
import os
from typing import Dict, Any, List, BinaryIO, Union

import magic

from src.apps.accounts.models import User
from src.apps.files.constants import ALLOWED_FORMATS
from src.apps.files.models import FilesStorage, File


def get_chunk_name(filename: str, chunk_number: int) -> str:
    return f'{filename}_part_{chunk_number}'


def extract_file_path(file: Union[str, File]) -> str:
    file_path = None
    if type(file) == str:
        file_path = file
    elif type(file) == File:
        file_path = file.destination
    return file_path


def is_valid_hash_md5(hash_sum: str, file: Union[str, BinaryIO, File]) -> bool:
    md5 = hashlib.md5()
    if type(file) == str or type(file) == File:
        file_path = extract_file_path(file)
        with open(file_path, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                md5.update(chunk)
            return hash_sum == md5.hexdigest()

    elif type(file) == BinaryIO:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            md5.update(chunk)
        return hash_sum == md5.hexdigest()

    else:
        return False


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


def is_valid_format(file: Union[str, BinaryIO, File]) -> bool:

    if type(file) == str or type(file) == File:
        file_path = extract_file_path(file)
        with open(file_path, 'r') as users_file:
            file = users_file.read(1024)
            file_type = magic.from_buffer(file, mime=True)
            return file_type in ALLOWED_FORMATS

    elif type(file) == BinaryIO:
        file_type = magic.from_buffer(file.read(1024), mime=True)
        return file_type in ALLOWED_FORMATS

    else:
        return False
