import os
from typing import Any, List

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.accounts.authentication import login_required
from src.accounts.models import User
from src.base.services.responses import CreatedResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.api.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.files.api.views.upload import get_chunk_name
from src.files.constants import FILE_STORAGE__TYPE__PERMANENT
from src.files.models import FilesStorage
from src.files.utils import create_file


def build_file(chunks_paths: List[str], filename) -> None:
    with open(filename, 'ab') as target_file:
        for path in chunks_paths:
            with open(path, 'rb') as stored_chunk_file:
                target_file.write(stored_chunk_file.read())
            os.unlink(path)


class BuildFileView(GenericAPIView):

    file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError()

        total_chunks = serializer.validated_data.get('total_chunks')
        filename = serializer.validated_data.get('filename')
        identifier = serializer.validated_data.get('identifier')

        temp_chunks_storage = os.path.join(self.file_storage.destination, str(user.id), identifier)
        file_path = os.path.join(self.file_storage, filename)
        chunks_paths = [
            os.path.join(temp_chunks_storage, get_chunk_name(filename, x))
            for x in range(1, total_chunks + 1)]

        upload_complete = all([os.path.exists(path) for path in chunks_paths])

        if upload_complete:
            build_file(chunks_paths, file_path)
            os.rmdir(temp_chunks_storage)

        create_file(user, self.file_storage, file_path, serializer.validated_data)
        return CreatedResponse({})
