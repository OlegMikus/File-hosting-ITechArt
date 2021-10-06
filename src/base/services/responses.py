from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from src.base.services.std_error_handler import generate_response


class CreatedResponse(Response):

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(generate_response(state=status.HTTP_201_CREATED, result=data, total_count=1))


class OkResponse(Response):

    def __init__(self, data: Dict[str, str] = None) -> None:
        super().__init__(generate_response(state=status.HTTP_200_OK, result=data, total_count=1))
