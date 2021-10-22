from django.urls import path

from src.files.api.views.build import BuildFileView
from src.files.api.views.upload import UploadView
from src.files.api.views.upload_template import UploadTemplateView
from src.files.api.views.upload_non_chunk import NonChunkUploadView

urlpatterns = [
    path('upload/', UploadTemplateView.as_view(), name='upload-template'),
    path('upload/chunks/', UploadView.as_view(), name='upload-chunks'),
    path('build/', BuildFileView.as_view(), name='build'),
    path('upload/non-chunk/', NonChunkUploadView.as_view(), name='upload-non-chunk')
]
