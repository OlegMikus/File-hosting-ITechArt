import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.base.services.responses import CreatedResponse
from src.base.services.std_error_handler import BadRequestError


class NonChunkUploadView(GenericAPIView):

    @login_required
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if not request.FILES.get('file'):
            raise BadRequestError()
        file_data = request.FILES.get('file')
        storage_path = os.path.expandvars('storage/permanent_storage/')
        to_file_path = os.path.join(storage_path, file_data.name)
        with open(to_file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)
        return CreatedResponse()
