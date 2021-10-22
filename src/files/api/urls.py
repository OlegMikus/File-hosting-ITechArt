from django.urls import path

from src.files.api.views.upload_non_chunk import NonChunkUploadView

urlpatterns = [
    path('upload/non-chunk/', NonChunkUploadView.as_view(), name='non-chunk-upload')
]
