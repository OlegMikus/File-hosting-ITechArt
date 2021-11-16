from typing import Callable

import pytest
from django.urls import reverse

from src.apps.accounts.models import User
from src.apps.accounts.serializers.user_serializer import UserSerializer
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserSignupView:

    def test_supports_post_request(self, api_client: APIClient) -> None:

        url = reverse('signup')
        data = {'username': 'TestUser',
                'password': 'A23$#fsfrwfwe'}
        response = api_client.post(url, data=data)

        assert response.status_code == 201

    def test_returns_400_when_password_is_missing(self, api_client: APIClient) -> None:

        url = reverse('signup')
        data = {'username': 'TestUser'}
        response = api_client.post(url, data=data)

        assert response.status_code == 400
        assert 'password' in response.data['data']['error_detail'][0].keys()


@pytest.mark.django_db
class TestUserLoginView:

    def test_supports_post_request(self, api_client: APIClient, create_user: Callable) -> None:

        url = reverse('login')
        user = create_user()
        data = {'username': user.username, 'password': 'Afe3#@vdfvrrcvs'}
        response = api_client.post(url, data=data)

        assert response.status_code == 200
        assert User.objects.count() == 1
        assert response.data['data']['result']['id'] == str(user.id)

    def test_returns_400_when_invalid_password(self, api_client: APIClient, create_user: Callable) -> None:

        url = reverse('login')
        user = create_user()
        data = {'username': user.username, 'password': 'dfkoijgdpfog'}
        response = api_client.post(url, data=data)

        assert response.status_code == 400
        assert User.objects.count() == 1
        assert response.data['data']['error_detail'] == ('Invalid username or password',)


@pytest.mark.django_db
class TestUserRefreshView:
    def test_supports_get_request(
            self, api_client: APIClient,
            create_token_for_user: Callable,
            create_user: Callable) -> None:

        url = reverse('refresh')
        api_client.credentials(HTTP_Refresh_Token=create_token_for_user(create_user()))
        response = api_client.get(url)

        assert response.status_code == 200

    def test_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('refresh')
        response = api_client.get(url)

        assert response.status_code == 401
        assert response.data['data']['error_detail'] == ('Missing token',)


@pytest.mark.django_db
class TestUserProfileView:

    def test_supports_get_request(
            self, create_token_for_user: Callable,
            create_user: Callable,
            api_client: APIClient) -> None:

        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(url)

        assert response.status_code == 200

    def test_get_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('profile')
        response = api_client.get(url)

        assert response.status_code == 401
        assert response.data['data']['error_detail'] == ('Missing token',)

    def test_supports_put_request(
            self, api_client: APIClient,
            create_token_for_user: Callable,
            create_user: Callable) -> None:

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

    def test_put_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('profile')
        api_client.credentials(HTTP_Access_Token=None)
        response = api_client.get(url)

        assert response.status_code == 401
        assert response.data['data']['result'] is None
        assert response.data['data']['error_detail'] == ('Missing token',)


@pytest.mark.django_db
class TestUserChangePasswordView:

    def test_pass_when_valid_data_passed(
            self, api_client: APIClient,
            create_user: Callable,
            create_token_for_user: Callable) -> None:

        url = reverse('change-password')

        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'Afe3#@vdfvrrcvs'
        }
        response = api_client.put(url, data)

        assert response.status_code == 200

    def test_fails_when_wrong_password_passed(
            self, api_client: APIClient,
            create_user: Callable,
            create_token_for_user: Callable) -> None:

        url = reverse('change-password')

        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'kbkbkujbjik'
        }
        response = api_client.put(url, data)

        assert response.status_code == 400
