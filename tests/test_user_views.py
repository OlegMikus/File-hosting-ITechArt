from typing import Tuple

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from src.apps.accounts.models import User
from src.apps.accounts.serializers.user_serializer import UserSerializer


class TestUserViews:
    @pytest.mark.django_db
    def test_signup_view(self,  api_client: APIClient) -> None:
        url = reverse('signup')
        data = {'username': 'TestUser',
                'password': 'A23$#fsfrwfwe'}
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_bad_signup_view(self, api_client: APIClient) -> None:
        url = reverse('signup')
        data = {'username': 'TestUser'}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert response.data['data']['error_detail'].key() == 'password'

    def test_login_view(self, create_user, test_password: str, api_client: APIClient) -> None:
        user = create_user()
        url = reverse('login')
        data = {'username': user.username,
                'password': test_password}
        response = api_client.post(url, data=data)
        assert response.status_code == 200
        assert response.data['data']['result']['id'] == str(user.id)

    def test_bad_login_view(self, create_user, api_client: APIClient) -> None:
        user = create_user()
        url = reverse('login')
        data = {'username': user.username,
                'password': 'dfkoijgdpfog'}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Invalid username or password',)

    def test_refresh_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('refresh')
        api_client.credentials(HTTP_Refresh_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 200

    def test_bad_refresh_view(self, api_client: APIClient) -> None:
        url = reverse('refresh')
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Missing token',)

    def test_profile_get_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 200

    def test_bad_profile_get_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Missing token',)

    def test_profile_put_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        data = {
            'first_name': 'test_user_name'
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        user = User.objects.get(id=create_token_for_user[1].id)
        assert response.data['data']['result'] == UserSerializer(user).data

    def test_bad_profile_put_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['result'] is None
        assert response.data['data']['error_detail'] == ('Missing token',)

    def test_change_password_view(self, test_password: str, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('change-password')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': test_password
        }
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_bad_change_password_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient) -> None:
        url = reverse('change-password')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'kbkbkujbjik'
        }
        response = api_client.put(url, data)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Wrong data',)
