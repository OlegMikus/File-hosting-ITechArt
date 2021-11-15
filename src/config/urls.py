from django.urls import path, include

from src.config.env_consts import APP_TYPE

urlpatterns = []

if APP_TYPE == 'AUTH':
    urlpatterns = [
        path('api/users/', include('src.apps.accounts.urls')),
    ]

if APP_TYPE == 'FILE':
    urlpatterns = [
        path('api/files/', include('src.apps.files.urls')),
    ]
