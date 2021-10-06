from typing import Any, Dict, Tuple

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class ForbiddenError(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(args[0])


class BadRequestError(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(args[0])


class NotFoundError(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(args[0])


def generate_response(error_detail: Tuple[Any, ...] = None,
                      state: status = None,
                      result: Dict[str, Any] = None,
                      total_count: int = 0) -> Dict[str, Any]:
    return {'data': {
        'status': state,
        'error_detail': error_detail,
        'result': result,
        'total_count': total_count
    }}


def std_error_handler(exc: Exception, context: Any) -> Response:
    if isinstance(exc, BadRequestError):
        print(exc.args)
        return Response(generate_response(error_detail=exc.args, state=status.HTTP_400_BAD_REQUEST))

    if isinstance(exc, NotFoundError):
        return Response(generate_response(error_detail=exc.args, state=status.HTTP_404_NOT_FOUND))

    if isinstance(exc, ForbiddenError):
        return Response(generate_response(error_detail=exc.args, state=status.HTTP_403_FORBIDDEN))

    if isinstance(exc, ValidationError):
        return Response(generate_response(error_detail=exc.args, state=status.HTTP_400_BAD_REQUEST))
