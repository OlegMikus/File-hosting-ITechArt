import os
import uuid
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import NotFoundError
from src.apps.files.models import File


class FileDownloadView(GenericAPIView):

    @login_required
    def get(self, request: Request, pk: uuid, *args: Any, user: User, **kwargs: Any) -> Response:
        file = File.objects.get(id=pk)
        file_path = file.absolute_path
        if not os.path.exists(file_path) or not file.user.id == user.id:
            raise NotFoundError('File does not exist')

        return Response(content_type='application/force-download',
                        headers={'Content-Disposition': f'attachment; filename:"{file.name}"',
                                 'X-Accel-Redirect': file_path})
