import os
from typing import Any

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import CreatedResponse
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.files.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT, FILE_STORAGE__TYPE__TEMP
from src.apps.files.models import FilesStorage
from src.apps.files.utils import is_upload_complete, get_chunk_name
from src.apps.files.tasks import task_build_file


class BuildFileView(GenericAPIView):

    perm_file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
    temp_file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)

    @login_required
    def post(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)

        total_chunks = serializer.validated_data.get('total_chunks')
        filename = serializer.validated_data.get('filename')
        identifier = serializer.validated_data.get('identifier')

        temp_chunks_storage = os.path.join(self.temp_file_storage.destination, str(user.id), identifier)

        chunks_paths = [
            os.path.join(temp_chunks_storage, get_chunk_name(filename, x))
            for x in range(1, total_chunks + 1)]

        if not is_upload_complete(chunks_paths):
            raise BadRequestError('Upload not finished')
        task_build_file.delay(user.id, self.perm_file_storage.id, serializer.validated_data,
                              chunks_paths, temp_chunks_storage)

        return CreatedResponse({})
