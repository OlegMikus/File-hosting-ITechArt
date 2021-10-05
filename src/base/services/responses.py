from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response


class CreatedResponse(Response):

    def __init__(self, data: Dict[str, Any]) -> None:
        data = {
            'id': data.get('id'),
            'email': data.get('email'),
            'age': data.get('age'),
        }
        data_content = {
            'data': {
                'status': status.HTTP_201_CREATED,
                'error_detail': None,
                'result': data,
                'total_count': 1
            }
        }
        super().__init__(data_content)


class OkResponse(Response):

    def __init__(self, data: Dict[str, str] = None) -> None:
        if 'access_token' in data.keys():
            data = {
                'user_id': data.get('id'),
                'access_token': data.get('access_token'),
                'refresh_token': data.get('refresh_token')
            }
        else:
            data = {
                'user_id': data.get('id')
            }
        data_content = {
            'data': {
                'status': status.HTTP_200_OK,
                'error_detail': None,
                'result': data,
                'total_count': 1
            }
        }
        super().__init__(data_content)
