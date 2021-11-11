from typing import Tuple

import pytest
from django.urls import reverse

from src.apps.accounts.models import User
from src.apps.accounts.serializers.user_serializer import UserSerializer


@pytest.mark.django_db
class TestUserSignupView:

    def test_signup_view(self, api_client) -> None:
        url = reverse('signup')
        data = {'username': 'TestUser',
                'password': 'A23$#fsfrwfwe'}
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    def test_bad_signup_view(self, api_client) -> None:
        url = reverse('signup')
        data = {'username': 'TestUser'}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert 'password' in response.data['data']['error_detail'][0].keys()


class TestUserLoginView:

    def test_login_view(self, api_client, create_user) -> None:
        url = reverse('login')
        user = create_user()
        data = {'username': user.username, 'password': 'Afe3#@vdfvrrcvs'}
        response = api_client.post(url, data=data)
        assert response.status_code == 200
        assert response.data['data']['result']['id'] == str(user.id)

    def test_bad_login_view(self, api_client, create_user) -> None:
        url = reverse('login')
        user = create_user()
        data = {'username': user.username, 'password': 'dfkoijgdpfog'}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Invalid username or password',)


class TestUserRefreshView:
    def test_refresh_view(self, api_client, create_token_for_user, create_user) -> None:
        url = reverse('refresh')
        api_client.credentials(HTTP_Refresh_Token=create_token_for_user(create_user()))
        response = api_client.get(url)
        assert response.status_code == 200

    def test_bad_refresh_view(self, api_client) -> None:
        url = reverse('refresh')
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Missing token',)


class TestUserProfileView:

    def test_profile_get_view(self, create_token_for_user, create_user, api_client) -> None:
        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(url)
        assert response.status_code == 200

    def test_bad_profile_get_view(self, api_client) -> None:
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Missing token',)

    def test_profile_put_view(self, api_client, create_token_for_user, create_user) -> None:
        url = reverse('profile')
        user = create_user()
        api_client.credentials(HTTP_Access_Token=create_token_for_user(user))
        data = {
            'first_name': 'test_user_name'
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        user = User.objects.get(id=user.id)
        assert response.data['data']['result'] == UserSerializer(user).data

    def test_bad_profile_put_view(self, api_client, create_token_for_user: Tuple[str, User]) -> None:
        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=None)
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['result'] is None
        assert response.data['data']['error_detail'] == ('Missing token',)


class TestUserChangePasswordView:

    def test_change_password_view(self, api_client, create_user, create_token_for_user) -> None:
        url = reverse('change-password')

        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'Afe3#@vdfvrrcvs'
        }
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_bad_change_password_view(self, api_client, create_user, create_token_for_user) -> None:
        url = reverse('change-password')

        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'kbkbkujbjik'
        }
        response = api_client.put(url, data)
        assert response.status_code == 400
        assert response.data['data']['error_detail'] == ('Wrong data',)
