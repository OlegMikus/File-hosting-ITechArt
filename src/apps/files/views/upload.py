import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import OkResponse, NotFoundResponse, CreatedResponse
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.files.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.apps.files.constants import FILE_STORAGE__TYPE__TEMP
from src.apps.files.models import FilesStorage
from src.apps.files.utils import get_chunk_name


class UploadView(GenericAPIView):

    file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)
    file_storage_path = file_storage.destination

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)

        if not serializer.is_valid():
            raise BadRequestError({})
        identifier = serializer.validated_data.get('identifier')
        filename = serializer.validated_data.get('filename')
        chunk_number = serializer.validated_data.get('chunk_number')

        temp_chunks_storage = os.path.join(self.file_storage_path, str(user.id), identifier)

        chunk_name = get_chunk_name(filename, chunk_number)
        chunk_path = os.path.join(temp_chunks_storage, chunk_name)

        if os.path.isfile(chunk_path):
            return OkResponse({})
        return NotFoundResponse({})

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)

        identifier = serializer.validated_data.get('identifier')
        filename = serializer.validated_data.get('filename')
        chunk_number = serializer.validated_data.get('chunk_number')

        chunk_data = request.FILES.get('file')
        temp_chunks_storage = os.path.join(self.file_storage_path, str(user.id), identifier)
        os.makedirs(temp_chunks_storage, 0o777, exist_ok=True)

        chunk_name = get_chunk_name(filename, chunk_number)
        chunk_path = os.path.join(temp_chunks_storage, chunk_name)

        with open(chunk_path, 'wb+') as file:
            for chunk in chunk_data.chunks():
                file.write(chunk)

        return CreatedResponse({})
