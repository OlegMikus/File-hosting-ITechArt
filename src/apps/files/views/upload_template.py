from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.authentication import login_required


class UploadTemplateView(GenericAPIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    @login_required
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response(template_name=self.template_name)
