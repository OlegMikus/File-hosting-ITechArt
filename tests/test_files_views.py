from typing import Callable

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from src.apps.files.models import File


@pytest.mark.django_db
class TestFileDashboardViews:
    def test_supports_get_request(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable) -> None:

        user = create_user()
        url = reverse('dashboard')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.get(url)

        assert response.status_code == 200

    def test_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('dashboard')
        response = api_client.get(url)

        assert response.status_code == 401


@pytest.mark.django_db
class TestFileUploadByChunksView:

    def test_returns_404_when_file_does_not_exist(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable) -> None:

        user = create_user()
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.get(
            url + '?resumableChunkNumber=1&resumableTotalSize=407644&resumableType=image%2Fjpeg&'
                  'resumableIdentifier=407644-nT1GuMCuM9Ijpg&resumableFilename=nT1GuMCuM9I.jpg&'
                  'resumableTotalChunks=1&resumableHash=hashChunk&resumableDescription=description')

        assert response.status_code == 404

    def test_post_returns_400_when_invalid_data(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable) -> None:

        user = create_user()
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.post(url)

        assert response.status_code == 400

    def test_get_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('upload-chunks')
        response = api_client.get(url)

        assert response.status_code == 401

    def test_post_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('upload-chunks')
        response = api_client.post(url)

        assert response.status_code == 401


@pytest.mark.django_db
class TestNonChinkUploadView:

    def test_post_returns_400_when_invalid_data(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable) -> None:

        user = create_user()
        url = reverse('upload-non-chunk')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.post(url, data={})

        assert response.status_code == 400

    def test_post_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('upload-non-chunk')
        response = api_client.post(url)

        assert response.status_code == 401


@pytest.mark.django_db
class TestDetailView:

    def test_supports_get_request(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable,
            create_file: Callable) -> None:

        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.get(url)

        assert response.status_code == 200
        expected_data = {'id': str(file.id), 'name': 'file.txt', 'description': ''}
        assert response.data['data']['result'] == expected_data

    def test_supports_put_request(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable,
            create_file: Callable) -> None:

        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        data = {'description': 'test file description'}
        response = api_client.put(url, data=data)

        assert response.status_code == 200
        expected_data = {'id': str(file.id), 'name': 'file.txt', 'description': 'test file description'}
        assert response.data['data']['result'] == expected_data

    def test_supports_delete_request(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable,
            create_file: Callable) -> None:

        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.delete(url)

        assert response.status_code == 200
        file = File.all_objects.filter(id=file.id).first()
        assert file.is_alive is False

    def test_get_returns_401_when_unauthenticated(
            self, api_client: APIClient, create_file: Callable,
            create_user: Callable) -> None:

        user = create_user()
        url = reverse('detail', kwargs={'primary_key': str(create_file(user).id)})
        response = api_client.get(url)

        assert response.status_code == 401
        assert response.data['data']['result'] is None

    def test_put_returns_401_when_unauthenticated(
            self, api_client: APIClient, create_file: Callable,
            create_user: Callable) -> None:

        user = create_user()
        url = reverse('detail', kwargs={'primary_key': str(create_file(user).id)})
        data = {'description': 'test file description'}

        response = api_client.put(url, data)

        assert response.status_code == 401
        assert response.data['data']['result'] is None

    def test_delete_returns_401_when_unauthenticated(
            self, api_client: APIClient, create_file: Callable,
            create_user: Callable) -> None:

        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        response = api_client.delete(url)

        assert response.status_code == 401
        file = File.all_objects.filter(id=file.id).first()
        assert file.is_alive is True


@pytest.mark.django_db
class TestUploadTemplateView:

    def test_supports_get_request(
            self, api_client: APIClient, create_user: Callable,
            create_token_for_user: Callable) -> None:

        user = create_user()
        url = reverse('upload-template')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.get(url)

        assert response.status_code == 200

    def test_returns_401_when_unauthenticated(self, api_client: APIClient) -> None:

        url = reverse('upload-template')
        response = api_client.get(url)

        assert response.status_code == 401


@pytest.mark.django_db
class TestDownloadSingleView:
    def test_returns_404_when_file_does_not_exist(
            self, create_token_for_user: Callable, create_user: Callable,
            api_client: APIClient,
            create_file: Callable) -> None:

        user = create_user()
        url = reverse('download-file', kwargs={'primary_key': str(create_file(user).id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(str(user.id)))
        response = api_client.get(url)

        assert response.status_code == 404
        assert 'X-Accel-Redirect' not in response.headers.keys()

    def test_returns_401_when_unauthenticated(
            self, create_file: Callable, create_user: Callable,
            api_client: APIClient) -> None:
        user = create_user()
        url = reverse('download-file', kwargs={'primary_key': str(create_file(user).id)})
        response = api_client.get(url)

        assert response.status_code == 401
