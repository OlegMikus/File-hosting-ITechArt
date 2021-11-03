import os
from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import BadRequestError, NotFoundError
from src.apps.files.models import File
from src.apps.files.serializers.file_serializer import FileSerializer


class FileDownloadView(GenericAPIView):

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        serializer = FileSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        file_id = serializer.validated_data.get('id')
        file = File.objects.get(id=file_id)
        file_path = file.absolute_path()
        if not os.path.exists(file_path):
            raise NotFoundError('file does not exist')
        if not file.user.id == user.id:
            raise BadRequestError('You do not have this file')

        return Response(content_type='application/force-download',
                        headers={'Content-Disposition': f'attachment; filename:"{str(user.username)}.zip"',
                                 'X-Accel-Redirect': file_path})
