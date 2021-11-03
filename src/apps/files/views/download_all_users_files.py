import os
import shutil
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import NotFoundError
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT, DOWNLOAD__ARCHIVE__TYPE, FILE_STORAGE__TYPE__TEMP
from src.apps.files.models import FilesStorage


class AllUsersFilesDownload(GenericAPIView):

    permanent_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
    temp_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        dir_with_files_to_archive = os.path.join(self.permanent_storage.destination, str(user.id))
        archive_into_this_dir = os.path.join(self.temp_storage.destination, str(user.id), str(user.username))

        if not os.path.exists(dir_with_files_to_archive) or len(os.listdir(dir_with_files_to_archive)) == 0:
            raise NotFoundError('Empty directory or its not exists')
        archive = shutil.make_archive(base_name=archive_into_this_dir, format=DOWNLOAD__ARCHIVE__TYPE,
                                      root_dir=dir_with_files_to_archive,
                                      base_dir='.')

        archive_path = os.path.join(archive_into_this_dir, archive)

        return Response(content_type='application/force-download',
                        headers={'Content-Disposition': f'attachment; filename:"{str(user.username)}.zip"',
                                 'X-Accel-Redirect': archive_path})
