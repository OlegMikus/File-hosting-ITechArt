from typing import Any

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.base.services.responses import OkResponse
from src.apps.files.models import File
from src.apps.files.paginator import CustomPagination
from src.apps.files.serializers.file_serializer import FileSerializer


class DashboardView(GenericAPIView):
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('name', 'size')
    search_fields = ('name', )
    pagination_class = CustomPagination
    serializer_class = FileSerializer

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> OkResponse:
        queryset = self.filter_queryset(queryset=File.objects.filter(user=user))
        serializer = self.serializer_class(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return OkResponse(data=page, total_count=len(queryset))
