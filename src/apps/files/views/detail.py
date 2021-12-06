from typing import Any
from uuid import UUID

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import OkResponse
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.files.models import File
from src.apps.files.serializers.file_serializer import FileSerializer
from src.apps.files.tasks import task_remove_file


class FileDetailView(GenericAPIView):
    serializer_class = FileSerializer

    @login_required
    def get(self, request: Request, *args: Any, primary_key: UUID, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.filter(id=primary_key, user=user).first()
        if not file:
            raise BadRequestError('File does not exist')
        serializer = self.serializer_class(file)
        return OkResponse(data=serializer.data)

    @login_required
    def put(self, request: Request, *args: Any, primary_key: UUID, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.filter(id=primary_key, user=user).first()
        serializer = self.serializer_class(file, data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)
        serializer.save()
        return OkResponse(data=serializer.data)

    @login_required
    def delete(self, request: Request, *args: Any, primary_key: UUID, user: User, **kwargs: Any) -> OkResponse:
        file = File.objects.filter(id=primary_key, user=user).first()
        if not file:
            raise BadRequestError('File does not exist')
        file.delete()
        task_remove_file.delay(file.absolute_path)
        return OkResponse(data={})
