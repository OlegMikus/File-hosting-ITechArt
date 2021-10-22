import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.accounts.models import User
from src.base.services.responses import CreatedResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.api.views.build import create_database_record
from src.files.constants import FILE_STORAGE__TYPE__PERMANENT, FILE__NON_CHUNK__MAX_SIZE
from src.files.utils import calculate_hash_md5
from src.files.models.files_storage import FilesStorage


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

        user_storage_dir = os.path.join(storage.destination, str(user.id))
        os.makedirs(user_storage_dir, exist_ok=True)

        file_path = os.path.join(user_storage_dir, file_data.name)

        with open(file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)

        actual_hash = calculate_hash_md5(file_path)

        if expected_hash != actual_hash:
            raise BadRequestError('Hash sum does not match')

        create_database_record(user, storage, file_path, request.data)
        return CreatedResponse({})
