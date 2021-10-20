import os
from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.base.services.responses import CreatedResponse
from src.base.services.std_error_handler import BadRequestError
from src.files.constants import FILE_STORAGE__TYPE__TEMP, FILE_STORAGE__TYPE__PERMANENT
from src.files.hash_count import hash_count
from src.files.models import File
from src.files.models.files_storage import FilesStorage


class NonChunkUploadView(GenericAPIView):

    @login_required
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if not request.FILES.get('file'):
            raise BadRequestError()
        storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
        user = kwargs.get('user')
        description = request.data.get('description')
        file_data = request.FILES.get('file')
        storage_dir = os.path.join(storage.destination, str(user.id))

        if not os.path.isdir(storage_dir):
            os.makedirs(storage_dir)

        to_file_path = os.path.join(storage_dir, file_data.name)

        with open(to_file_path, 'wb+') as file:
            for chunk in file_data.chunks():
                file.write(chunk)

        files_hash = hash_count(to_file_path)
        print(files_hash)

        file = File.objects.create(user=user,
                                   storage=storage,
                                   destination=to_file_path,
                                   name=file_data.name[0:-4],
                                   description=description,
                                   type=file_data.name[-4:],
                                   size=file_data.size,
                                   hash=files_hash)
        file.save()

        return CreatedResponse({'response': 'nice'})
