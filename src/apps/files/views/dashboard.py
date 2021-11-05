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
    ordering_fields = ('name',)
    pagination_class = CustomPagination

    # @login_required
    def get(self, request: Request, *args: Any, **kwargs: Any) -> OkResponse:
        user = User.objects.get(id='02c1ed06-43a8-458f-808d-d621fed0128c')
        queryset = self.filter_queryset(queryset=File.objects.filter(user=user))
        print(queryset)
        serializer = FileSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return OkResponse(page)
