from django.urls import path

from src.apps.files.views.download_all_users_files import AllUsersFilesDownload
from src.apps.files.views.download_single_file import FileDownloadView
from src.apps.files.views.file_build_view import BuildFileView
from src.apps.files.views.upload import UploadView
from src.apps.files.views.upload_template import UploadTemplateView
from src.apps.files.views.upload_non_chunk import NonChunkUploadView

urlpatterns = [
    path('upload/', UploadTemplateView.as_view(), name='upload-template'),
    path('upload/chunks/', UploadView.as_view(), name='upload-chunks'),
    path('build/', BuildFileView.as_view(), name='build'),
    path('upload/non-chunk/', NonChunkUploadView.as_view(), name='upload-non-chunk'),
    path('download/<uuid:pk>/', FileDownloadView.as_view(), name='download-file'),
    path('download/', AllUsersFilesDownload.as_view(), name='download-all-files'),

]
