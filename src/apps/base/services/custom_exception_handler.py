from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler

from src.apps.base.services.std_error_handler import std_error_handler


def custom_exception_handler(exc: Exception, context: Any) -> Response:
    response = std_error_handler(exc, context)
    if response is None:
        response = exception_handler(exc, context)
    return response
