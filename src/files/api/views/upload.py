from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.base.services.responses import OkResponse


class UploadView(GenericAPIView):

    def get(self, request: Request, *args: Any, **kwargs: Any) -> OkResponse:
        return OkResponse({'message': 'Upload view working'})
