import io
import os
import shutil
from typing import Tuple, Dict, Any
from rest_framework.test import APIClient
from django.urls import reverse

from src.apps.accounts.models import User
from src.apps.files.constants import FILE_STORAGE__TYPE__TEMP, FILE_STORAGE__TYPE__PERMANENT
from src.apps.files.models import File, FilesStorage
from src.apps.files.serializers.file_serializer import FileSerializer


class TestFileViews:
    def test_dashboard_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User]) -> None:
        url = reverse('dashboard')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 200

    def test_upload_chunks_get_view_authenticate(self, api_client: APIClient,
                                                 create_token_for_user: Tuple[str, User]) -> None:
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(
            url + '?resumableChunkNumber=1&resumableTotalSize=407644&resumableType=image%2Fjpeg&'
                  'resumableIdentifier=407644-nT1GuMCuM9Ijpg&resumableFilename=nT1GuMCuM9I.jpg&'
                  'resumableTotalChunks=1&resumableHash=hashChunk&resumableDescription=description')
        assert response.status_code == 404

    def test_upload_chunks_post_view_authenticate(self, api_client: APIClient,
                                                  create_token_for_user: Tuple[str, User]) -> None:
        url = reverse('upload-chunks')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        data = {
            'file': (io.BytesIO(b"some initial text data"), 'file.txt')
        }
        response = api_client.post(url + '?resumableChunkNumber=1&resumableTotalSize=1&resumableType=text/plain&'
                                         'resumableIdentifier=407644-filetxt&resumableFilename=file.txt&'
                                         'resumableTotalChunks=1&resumableHash=1&resumableDescription=test',
                                   data=data)
        file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__TEMP)
        shutil.rmtree(os.path.join(file_storage.destination, str(create_token_for_user[1].id)))
        assert response.status_code == 201

    def test_upload_non_chunks_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User],
                                                 create_upload_file_data: Dict[str, Any]) -> None:
        url = reverse('upload-non-chunk')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.post(url, data=create_upload_file_data)
        file_storage = FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT)
        shutil.rmtree(os.path.join(file_storage.destination, str(create_token_for_user[1].id)))
        assert response.status_code == 201

    def test_detail_get_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User],
                                          create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['data']['result'] == FileSerializer(create_file).data

    def test_detail_put_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User],
                                          create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        data = {'description': 'test file description'}
        response = api_client.put(url, data)
        assert response.status_code == 200
        file = File.all_objects.filter(name='file.txt').first()
        assert response.data['data']['result'] == FileSerializer(file).data

    def test_detail_delete_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User],
                                             create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.delete(url)
        assert response.status_code == 200
        file = File.all_objects.filter(name='file.txt').first()
        assert file.is_alive is False

    def test_upload_view_authenticate(self, api_client: APIClient, create_token_for_user: Tuple[str, User]) -> None:
        url = reverse('upload-template')
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 200

    def test_dashboard_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('dashboard')
        response = api_client.get(url)
        assert response.status_code == 400

    def test_upload_chunks_get_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-chunks')
        response = api_client.get(url + '?resumableChunkNumber=1&resumableTotalSize=407644&resumableType=image%2Fjpeg&'
                                        'resumableIdentifier=407644-nT1GuMCuM9Ijpg&resumableFilename=nT1GuMCuM9I.jpg&'
                                        'resumableTotalChunks=1&resumableHash=hashChunk&'
                                        'resumableDescription=description')
        assert response.status_code == 400

    def test_upload_chunks_post_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-chunks')
        data = {
            'file': (io.BytesIO(b"some initial text data"), 'file.txt')
        }
        response = api_client.post(url + '?resumableChunkNumber=1&resumableTotalSize=407644&resumableType=image%2Fjpeg&'
                                         'resumableIdentifier=407644-nT1GuMCuM9Ijpg&resumableFilename=nT1GuMCuM9I.jpg&'
                                         'resumableTotalChunks=1&resumableHash=hashChunk&'
                                         'resumableDescription=description',
                                   data=data)
        assert response.status_code == 400

    def test_upload_non_chunks_view_unauthenticated(self, api_client: APIClient,
                                                    create_upload_file_data: Dict[str, Any]) -> None:
        url = reverse('upload-non-chunk')
        response = api_client.post(url, data=create_upload_file_data)
        assert response.status_code == 400

    def test_detail_get_view_unauthenticated(self, api_client: APIClient, create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        response = api_client.get(url)
        assert response.status_code == 400
        assert response.data['data']['result'] is None

    def test_detail_put_view_unauthenticated(self, api_client: APIClient, create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        data = {'description': 'test file description'}

        response = api_client.put(url, data)
        assert response.status_code == 400
        assert response.data['data']['result'] is None

    def test_detail_delete_view_unauthenticated(self, api_client: APIClient, create_file: File) -> None:
        url = reverse('detail', kwargs={'primary_key': str(create_file.id)})
        response = api_client.delete(url)
        file = File.all_objects.filter(name='file.txt').first()
        assert response.status_code == 400
        assert file.is_alive is True

    def test_upload_view_unauthenticated(self, api_client: APIClient) -> None:
        url = reverse('upload-template')
        response = api_client.get(url)
        assert response.status_code == 400

    def test_fail_download_single_file_view(self, create_token_for_user: Tuple[str, User], api_client: APIClient, create_file: File) -> None:
        url = reverse('download-file', kwargs={'primary_key': create_file.id})
        api_client.credentials(HTTP_Access_Token=create_token_for_user[0])
        response = api_client.get(url)
        assert response.status_code == 404
        assert 'X-Accel-Redirect' not in response.headers.keys()

    def test_fail_download_single_file_view_unauthenticated(self, create_token_for_user: Tuple[str, User], api_client: APIClient, create_file: File) -> None:
        url = reverse('download-file', kwargs={'primary_key': create_file.id})
        response = api_client.get(url)
        assert response.status_code == 400
