import os
import uuid

from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from src.base.services.responses import OkResponse
from src.base.services.std_error_handler import BadRequestError


def get_chunk_name(uploaded_filename, chunk_number):
    return uploaded_filename + "_part_%03d" % chunk_number


class UploadView(GenericAPIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'templates/index.html'

    def get(self, request):
        return Response(template_name='index.html')


class RealUploadView(GenericAPIView):

    file_storage = os.path.expandvars('media/upload/')

    def get(self, request: Request, *args, **kwargs):

        resumable_identifier = request.query_params.get('resumableIdentifier')
        resumable_filename = request.query_params.get('resumableFilename')
        resumable_chunk_number = int(request.query_params.get('resumableChunkNumber'))

        if not resumable_identifier or not resumable_filename or not resumable_chunk_number:
            return HttpResponse(500, 'Parameter error')  # TODO: fix this response

        temp_files_chunks_storage = os.path.join(self.file_storage, resumable_identifier)

        chunk_name = get_chunk_name(resumable_filename, resumable_chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        if os.path.isfile(path_to_store_chunk):
            return OkResponse({'info': 'this chunk already exists'})
        else:
            return BadRequestError({'info': 'this chunk does not exists and needs to be uploaded'})

    def post(self, request, *args, **kwargs):
        resumable_total_chunks = int(request.query_params.get('resumableTotalChunks'))
        resumable_chunk_number = int(request.query_params.get('resumableChunkNumber'))
        resumable_filename = request.query_params.get('resumableFilename')
        resumable_identifier = request.query_params.get('resumableIdentifier')

        chunk_data = request.FILES.get('file')

        temp_files_chunks_storage = os.path.join(self.file_storage, resumable_identifier)
        if not os.path.isdir(temp_files_chunks_storage):
            os.makedirs(temp_files_chunks_storage)

        chunk_name = get_chunk_name(resumable_filename, resumable_chunk_number)
        path_to_store_chunk = os.path.join(temp_files_chunks_storage, chunk_name)

        with open(path_to_store_chunk, 'wb+') as f:
            for chunk in chunk_data.chunks():
                f.write(chunk)

        chunks_paths_list = [os.path.join(temp_files_chunks_storage, get_chunk_name(resumable_filename, x)) for x in range(1, resumable_total_chunks + 1)]
        upload_complete = all([os.path.exists(path) for path in chunks_paths_list])

        if upload_complete:
            target_file_name = os.path.join(self.file_storage, resumable_filename)
            with open(target_file_name, "ab") as target_file:
                for path in chunks_paths_list:
                    stored_chunk_file_name = path
                    stored_chunk_file = open(stored_chunk_file_name, 'rb')
                    target_file.write(stored_chunk_file.read())
                    stored_chunk_file.close()
                    os.unlink(stored_chunk_file_name)
            target_file.close()
            os.rmdir(temp_files_chunks_storage)

        return OkResponse()
