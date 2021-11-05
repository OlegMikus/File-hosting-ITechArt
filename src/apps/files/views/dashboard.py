from typing import Any

from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import OkResponse
from src.apps.files.models import File
from src.apps.files.serializers.file_serializer import FileSerializer


class DashboardView(GenericAPIView):
    ordering_fields = ('date_updated', 'name', 'size')
    pagination_class = PageNumberPagination
    filter_backends = OrderingFilter
    pagination_class.page_size = 4

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> OkResponse:
        queryset = File.objects.filter(user=user)
        serializer = FileSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return OkResponse(page)
