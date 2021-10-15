import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.base.services.responses import OkResponse, NotFoundResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.api.serializers.query_params_serializer import QuerySerializer


def get_chunk_name(uploaded_filename, chunk_number):
    return uploaded_filename + f'_part_{chunk_number}'


class UploadView(GenericAPIView):

    file_storage = os.path.expandvars('file_storage')

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = QuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError()

        identifier = serializer.data.get('resumableIdentifier')
        filename = serializer.data.get('resumableFilename')
        chunk_number = serializer.data.get('resumableChunkNumber')

        temp_files_chunks_storage = os.path.join(self.file_storage, identifier)

        chunk_name = get_chunk_name(filename, chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        if os.path.isfile(path_to_store_chunk):
            return OkResponse()
        return NotFoundResponse()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = QuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError()

        identifier = serializer.data.get('resumableIdentifier')
        filename = serializer.data.get('resumableFilename')
        chunk_number = serializer.data.get('resumableChunkNumber')

        chunk_data = request.FILES.get('file')
        temp_files_chunks_storage = os.path.join(self.file_storage, identifier)
        if not os.path.isdir(temp_files_chunks_storage):
            os.makedirs(temp_files_chunks_storage)

        chunk_name = get_chunk_name(filename, chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        with open(path_to_store_chunk, 'wb+') as file:
            for chunk in chunk_data.chunks():
                file.write(chunk)

        return OkResponse()
