import uuid
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import OkResponse
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.files.models import File
from src.apps.files.serializers.file_serializer import FileSerializer


class FileDetailView(GenericAPIView):

    @login_required
    def get(self, request: Request, *args: Any, pk: uuid, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.get(id=pk, user=user)
        if not file:
            raise BadRequestError('File does not exist')
        serializer = FileSerializer(file)
        return OkResponse(serializer.data)

    @login_required
    def put(self, request: Request, *args: Any, pk: uuid, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.get(id=pk, user=user)
        serializer = FileSerializer(file, data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)
        serializer.save()
        return OkResponse(serializer.data)

    @login_required
    def delete(self, request: Request, *args: Any, pk: uuid, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.get(id=pk, user=user)
        if not file:
            raise BadRequestError('File does not exist')
        file.is_alive = False
        file.save()
        return OkResponse({})
