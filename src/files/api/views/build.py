import os
from typing import Any

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.base.services.responses import OkResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.api.serializers.query_params_serializer import ChunkUploadQueryParamsSerializer
from src.files.api.views.upload import get_chunk_name


class BuildFileView(GenericAPIView):

    file_storage = os.path.expandvars('file_storage')

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ChunkUploadQueryParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise BadRequestError()
        total_chunks = serializer.data.get('resumableTotalChunks')
        filename = serializer.data.get('resumableFilename')
        identifier = serializer.data.get('resumableIdentifier')

        temp_files_chunks_storage = os.path.join(self.file_storage, identifier)

        chunks_paths = [
            os.path.join(temp_files_chunks_storage, get_chunk_name(filename, x))
            for x in range(1, total_chunks + 1)]
        upload_complete = all([os.path.exists(path) for path in chunks_paths])

        if upload_complete:
            target_file_name = os.path.join(self.file_storage, filename)
            with open(target_file_name, 'ab') as target_file:
                for path in chunks_paths:
                    with open(path, 'rb') as stored_chunk_file:
                        target_file.write(stored_chunk_file.read())
                    stored_chunk_file.close()
                    os.unlink(path)
            target_file.close()
            os.rmdir(temp_files_chunks_storage)

        return OkResponse()
