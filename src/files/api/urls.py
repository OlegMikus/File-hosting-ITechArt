from django.urls import path

from src.files.api.views.download import DownloadView
from src.files.api.views.upload import UploadView

urlpatterns = [
    path('download/', DownloadView.as_view(), name='download'),
    path('upload/', UploadView.as_view(), name='upload'),
]
