from typing import Callable

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from src.apps.files.models import File
from src.apps.files.serializers.file_serializer import FileSerializer


@pytest.mark.django_db
class TestFileDashboardViews:
    def test_dashboard_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                         create_token_for_user: Callable) -> None:
        url = reverse('dashboard')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(url)
        assert response.status_code == 200

    def test_dashboard_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('dashboard')
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestFileUploadByChunksView:

    def test_upload_chunks_get_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                                 create_token_for_user: Callable) -> None:
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(
            url + '?resumableChunkNumber=1&resumableTotalSize=407644&resumableType=image%2Fjpeg&'
                  'resumableIdentifier=407644-nT1GuMCuM9Ijpg&resumableFilename=nT1GuMCuM9I.jpg&'
                  'resumableTotalChunks=1&resumableHash=hashChunk&resumableDescription=description')
        assert response.status_code == 404

    def test_upload_chunks_post_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                                  create_token_for_user: Callable) -> None:
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.post(url)
        assert response.status_code == 400

    def test_upload_chunks_get_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-chunks')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_upload_chunks_post_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-chunks')
        response = api_client.post(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestNonChinkUploadView:

    def test_upload_non_chunks_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                                 create_token_for_user: Callable) -> None:
        url = reverse('upload-non-chunk')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.post(url, data={})
        assert response.status_code == 400

    def test_upload_non_chunks_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-non-chunk')
        response = api_client.post(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestDetailView:

    def test_detail_get_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                          create_token_for_user: Callable,
                                          create_file: Callable) -> None:
        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(user))
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['data']['result'] == FileSerializer(file).data

    def test_detail_put_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                          create_token_for_user: Callable,
                                          create_file: Callable) -> None:
        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(user))
        data = {'description': 'test file description'}
        response = api_client.put(url, data=data)
        assert response.status_code == 200
        file = File.all_objects.filter(id=file.id).first()
        assert response.data['data']['result'] == FileSerializer(file).data

    def test_detail_delete_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                             create_token_for_user: Callable,
                                             create_file: Callable) -> None:
        user = create_user()
        file = create_file(user)
        url = reverse('detail', kwargs={'primary_key': str(file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(user))
        response = api_client.delete(url)
        assert response.status_code == 200
        file = File.all_objects.filter(id=file.id).first()
        assert file.is_alive is False

    def test_detail_get_view_unauthenticated(self, api_client: APIClient, create_file: Callable,
                                             create_user: Callable) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file(create_user()).id)})
        response = api_client.get(url)
        assert response.status_code == 401
        assert response.data['data']['result'] is None

    def test_detail_put_view_unauthenticated(self, api_client: APIClient, create_file: Callable,
                                             create_user: Callable) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file(create_user()).id)})
        data = {'description': 'test file description'}

        response = api_client.put(url, data)
        assert response.status_code == 401
        assert response.data['data']['result'] is None

    def test_detail_delete_view_unauthenticated(self, api_client: APIClient, create_file: Callable,
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

    def test_upload_view_authenticate(self, api_client: APIClient, create_user: Callable,
                                      create_token_for_user: Callable) -> None:
        url = reverse('upload-template')
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(url)
        assert response.status_code == 200

    def test_upload_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-template')
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestDownloadSingleView:
    def test_fail_download_single_file_view(self, create_token_for_user: Callable, create_user: Callable,
                                            api_client: APIClient,
                                            create_file: Callable) -> None:
        url = reverse('download-file', kwargs={'primary_key': str(create_file(create_user()).id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user(create_user()))
        response = api_client.get(url)
        assert response.status_code == 404
        assert 'X-Accel-Redirect' not in response.headers.keys()

    def test_fail_download_single_file_view_unauthenticated(self, create_file: Callable, create_user: Callable,
                                                            api_client: APIClient) -> None:
        url = reverse('download-file', kwargs={'primary_key': str(create_file(create_user()).id)})
        response = api_client.get(url)
        assert response.status_code == 401