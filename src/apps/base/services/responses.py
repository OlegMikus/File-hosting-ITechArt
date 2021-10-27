from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from src.apps.base.services.std_error_handler import generate_response


class CreatedResponse(Response):

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data=generate_response(result=data, total_count=1),
                         status=status.HTTP_201_CREATED)


class OkResponse(Response):

    def __init__(self, data: Dict[str, str]) -> None:

        super().__init__(data=generate_response(result=data, total_count=1),
                         status=status.HTTP_200_OK,)


class NotFoundResponse(Response):

    def __init__(self, data: Dict[str, str]) -> None:
        super().__init__(data=generate_response(result=data, total_count=0),
                         status=status.HTTP_404_NOT_FOUND)
