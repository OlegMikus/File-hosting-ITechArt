from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from src.apps.base.services.std_error_handler import generate_response


class CreatedResponse(Response):

    def __init__(self, data: Dict[str, Any], total_count: int = 1) -> None:
        super().__init__(data=generate_response(result=data, total_count=total_count),
                         status=status.HTTP_201_CREATED)


class OkResponse(Response):

    def __init__(self, data: Dict[str, str], total_count: int = 1) -> None:

        super().__init__(data=generate_response(result=data, total_count=total_count),
                         status=status.HTTP_200_OK,)


class NotFoundResponse(Response):

    def __init__(self, data: Dict[str, str], total_count: int = 0) -> None:
        super().__init__(data=generate_response(result=data, total_count=total_count),
                         status=status.HTTP_404_NOT_FOUND)
