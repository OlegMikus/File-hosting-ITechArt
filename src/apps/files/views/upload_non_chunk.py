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
from src.apps.files.utils import create_file, is_valid_format, is_valid_hash_md5
from src.apps.files.models.files_storage import FilesStorage


class NonChunkUploadView(GenericAPIView):
    storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        if not request.FILES.get('file'):
            raise BadRequestError('File is missing')

        hash_sum = request.data.get('hash_sum')
        file_data = request.FILES.get('file')

        if file_data.size > FILE__NON_CHUNK__MAX_SIZE:
            raise BadRequestError('File is too large')

        user_storage_dir = os.path.join(self.storage.destination, str(user.id))
        os.makedirs(user_storage_dir, 0o777, exist_ok=True)

        file_path = os.path.join(user_storage_dir, file_data.name)

        with open(file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)

        errors = []
        if not is_valid_format(file_path):
            errors.append(f'Unsupported file format, use one from this: {ALLOWED_FORMATS}')
        if not is_valid_hash_md5(request.data.get('total_size'), hash_sum, file_path):
            errors.append('Invalid hash')
        if errors:
            os.remove(file_path)
            raise BadRequestError(errors)

        create_file(user, self.storage, request.data)
        return CreatedResponse({})
