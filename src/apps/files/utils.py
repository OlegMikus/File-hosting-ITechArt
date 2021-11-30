import hashlib
import os
from typing import Dict, Any, List

import magic
from django.core.mail import send_mail

from src.apps.accounts.models import User
from src.apps.files.constants import ALLOWED_FORMATS, \
    SMALL_FILE_MAX_SIZE, \
    FILE__FIRST_SLICE, \
    FILE__SECOND_SLICE
from src.apps.files.models import FilesStorage, File
from src.config.env_consts import DJANGO_DEFAULT_FROM_EMAIL, \
    DJANGO_EMAIL_HOST_PASSWORD, \
    DJANGO_EMAIL_HOST_USER


def send_email(title: str, message: Any, recipients: List[str]) -> None:
    send_mail(subject=title, message=message, from_email=DJANGO_DEFAULT_FROM_EMAIL, recipient_list=recipients,
              auth_user=DJANGO_EMAIL_HOST_USER, auth_password=DJANGO_EMAIL_HOST_PASSWORD)


def get_chunk_name(filename: str, chunk_number: int) -> str:
    return f'{filename}_part_{chunk_number}'


def is_valid_hash_md5(file_size: str, hash_sum: str, file_path: str) -> bool:
    md5 = hashlib.md5()
    if not file_path:
        return False

    if int(file_size) > SMALL_FILE_MAX_SIZE:
        with open(file_path, 'rb') as file:
            md5.update(file.read(FILE__FIRST_SLICE))
            md5.update(file.read()[-FILE__SECOND_SLICE:])
        return hash_sum == md5.hexdigest()

    with open(file_path, 'rb') as file:
        chunk = None
        while chunk != b'':
            chunk = file.read(1024)
            md5.update(chunk)
        return hash_sum == md5.hexdigest()


def create_file(user: User,
                storage: FilesStorage,
                data: Dict[str, Any]
                ) -> None:
    user_storage_dir = os.path.join(str(user.id), data.get('filename'))
    File.objects.create(user=user, storage=storage,
                        destination=user_storage_dir, name=data.get('filename'),
                        description=data.get('description'), type=data.get('extension'),
                        size=data.get('total_size'), hash=data.get('hash_sum'))


def is_upload_complete(chunks_paths: List[str]) -> bool:
    return all([os.path.exists(path) for path in chunks_paths])


def is_valid_format(file_path: str) -> bool:
    if not file_path:
        return False

    with open(file_path, 'rb') as users_file:
        file = users_file.read(1024)
        file_type = magic.from_buffer(file, mime=True)
        return file_type in ALLOWED_FORMATS
