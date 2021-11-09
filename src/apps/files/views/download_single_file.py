import os
from typing import Any
from uuid import UUID

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import NotFoundError
from src.apps.files.models import File


class FileDownloadView(GenericAPIView):

    @login_required
    def get(self, request: Request, primary_key: UUID, *args: Any, user: User, **kwargs: Any) -> Response:
        file = File.objects.filter(id=primary_key, user=user).first()

        if not file or not os.path.isfile(file.absolute_path):
            raise NotFoundError('File does not exist')
        file_path = file.destination
        return Response(content_type='application/force-download',
                        headers={'Content-Disposition': f'attachment; filename:"{file.name}"',
                                 'X-Accel-Redirect': file_path})
