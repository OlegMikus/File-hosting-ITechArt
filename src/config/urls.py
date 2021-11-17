from django.urls import path, include

from src.config.env_consts import APP_TYPE, APP_TYPE_FILE, APP_TYPE_AUTH, ENVIRONMENT

urlpatterns = []

auth_urls = [
    path('api/users/', include('src.apps.accounts.urls')),
]

file_urls = [
    path('api/files/', include('src.apps.files.urls')),
]

if APP_TYPE == APP_TYPE_AUTH:
    urlpatterns = auth_urls

if APP_TYPE == APP_TYPE_FILE:
    urlpatterns = file_urls

if ENVIRONMENT == 'testing':
    urlpatterns = auth_urls + file_urls
