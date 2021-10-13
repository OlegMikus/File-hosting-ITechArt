from django.urls import path

from src.files.api.views.upload import RealUploadView, UploadView
from src.files.api.views.upload_non_chunk import NonChunkUploadView

urlpatterns = [
    path('api/upload/', UploadView.as_view(), name='upload-view'),
    path('upload/', RealUploadView.as_view(), name='upload'),
    path('upload/non-chunk/', NonChunkUploadView.as_view(), name='non-chunk-upload')
]
