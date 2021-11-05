import os
import shutil
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import NotFoundError
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT, ARCHIVE__TYPE, FILE_STORAGE__TYPE__TEMP, \
    USER_STORAGE__LOCATION__NGINX
from src.apps.files.models import FilesStorage


class AllUsersFilesDownload(GenericAPIView):

    permanent_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
    temp_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:
        dir_to_archive = os.path.join(self.permanent_storage.destination, str(user.id))
        archive_dir = os.path.join(self.temp_storage.destination, str(user.id), str(user.username))

        if not os.path.exists(dir_to_archive) or len(os.listdir(dir_to_archive)) == 0:
            raise NotFoundError('Empty directory or its not exists')
        shutil.make_archive(base_name=archive_dir, format=ARCHIVE__TYPE, root_dir=dir_to_archive, base_dir='.')

        filename = f'{str(user.username)}.{ARCHIVE__TYPE}'
        archive_path = os.path.join(USER_STORAGE__LOCATION__NGINX, str(user.id), filename)

        return Response(content_type='application/force-download',
                        headers={'Content-Disposition': f'attachment; filename:"{filename}"',
                                 'X-Accel-Redirect': archive_path})