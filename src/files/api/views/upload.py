import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.accounts.models import User
from src.base.services.responses import OkResponse, NotFoundResponse, CreatedResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.api.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.files.constants import FILE_STORAGE__TYPE__TEMP
from src.files.models import FilesStorage


def get_chunk_name(uploaded_filename: str, chunk_number: int) -> str:
    return f'{uploaded_filename}_part_{chunk_number}'


class UploadView(GenericAPIView):

    file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)
    file_storage_path = file_storage.destination

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)

        if not serializer.is_valid():
            raise BadRequestError()
        identifier = serializer.validated_data.get('identifier')
        filename = serializer.validated_data.get('filename')
        chunk_number = serializer.validated_data.get('chunk_number')

        temp_files_chunks_storage = os.path.join(self.file_storage_path, str(user.id), identifier)

        chunk_name = get_chunk_name(filename, chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        if os.path.isfile(path_to_store_chunk):
            return OkResponse({})
        return NotFoundResponse({})

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError()

        identifier = serializer.validated_data.get('identifier')
        filename = serializer.validated_data.get('filename')
        chunk_number = serializer.validated_data.get('chunk_number')

        chunk_data = request.FILES.get('file')
        temp_files_chunks_storage = os.path.join(self.file_storage_path, str(user.id), identifier)
        os.makedirs(temp_files_chunks_storage, exist_ok=True)

        chunk_name = get_chunk_name(filename, chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        with open(path_to_store_chunk, 'wb+') as file:
            for chunk in chunk_data.chunks():
                file.write(chunk)

        return CreatedResponse({})
