import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import CreatedResponse
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT, FILE__NON_CHUNK__MAX_SIZE, ALLOWED_FORMATS
from src.apps.files.utils import calculate_hash_md5, create_file, is_valid_format
from src.apps.files.models.files_storage import FilesStorage


class NonChunkUploadView(GenericAPIView):

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        if not request.FILES.get('file'):
            raise BadRequestError('File is missing')

        storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
        expected_hash = request.data.get('hash_sum')
        file_data = request.FILES.get('file')

        if file_data.size > FILE__NON_CHUNK__MAX_SIZE:
            raise BadRequestError('File is too large')

        actual_hash = calculate_hash_md5(file_data)

        if expected_hash != actual_hash:
            raise BadRequestError('Hash sum does not match')

        user_storage_dir = os.path.join(storage.destination, str(user.id))
        os.makedirs(user_storage_dir, 0o777, exist_ok=True)

        file_path = os.path.join(user_storage_dir, file_data.name)

        with open(file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)

        if not is_valid_format(file_path):
            os.remove(file_path)
            raise BadRequestError(f'Unsupported file format, use one from this: {ALLOWED_FORMATS}')

        create_file(user, storage, file_path, request.data)
        return CreatedResponse({})
