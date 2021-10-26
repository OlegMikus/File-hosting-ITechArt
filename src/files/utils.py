import hashlib
from typing import Dict, Any

from src.accounts.models import User
from src.files.models import FilesStorage, File


def calculate_hash_md5(file_path):
    md5 = hashlib.md5()

    with open(file_path, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
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
