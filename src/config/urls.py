from django.urls import path, include

from src.config.env_consts import APP_TYPE, APP_TYPE_FILE, APP_TYPE_AUTH

urlpatterns = []

if APP_TYPE == APP_TYPE_AUTH:
    urlpatterns = [
        path('api/users/', include('src.apps.accounts.urls')),
    ]

if APP_TYPE == APP_TYPE_FILE:
    urlpatterns = [
        path('api/files/', include('src.apps.files.urls')),
    ]
