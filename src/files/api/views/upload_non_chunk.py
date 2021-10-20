import os
from typing import Any, Tuple

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.accounts.models import User
from src.base.services.responses import CreatedResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.constants import FILE_STORAGE__TYPE__PERMANENT
from src.files.hash_count import calculate_hash_md5
from src.files.models import File
from src.files.models.files_storage import FilesStorage


def get_filename_and_type(data: str) -> Tuple[str, str]:
    filename, file_type = data.split('.')
    return filename, file_type


class NonChunkUploadView(GenericAPIView):

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        if not request.FILES.get('file'):
            raise BadRequestError('File is missing')

        storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
        hash_from_request = request.data.get('hash')
        description = request.data.get('description')
        file_data = request.FILES.get('file')

        user_storage_dir = os.path.join(storage.destination, str(user.id))
        os.makedirs(user_storage_dir, exist_ok=True)

        to_file_path = os.path.join(user_storage_dir, file_data.name)

        with open(to_file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)

        files_hash = calculate_hash_md5(to_file_path)
        filename, file_type = get_filename_and_type(file_data.name)

        if hash_from_request != files_hash:
            raise BadRequestError('Hash sum do not match')

        File.objects.create(user=user, storage=storage,
                            destination=to_file_path, name=filename,
                            description=description, type=file_type,
                            size=file_data.size, hash=files_hash)

        return CreatedResponse({'response': 'created'})  # TODO: fix this after merge
