from django.conf.urls import url
from django.urls import path, include
from src.apps.base.swagger_view import SchemaView
from src.config.env_consts import APP_TYPE, APP_TYPE_FILE, APP_TYPE_AUTH, ENVIRONMENT

urlpatterns = []


swagger_urls = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
auth_urls = [
    path('api/users/', include('src.apps.accounts.urls')),
]

file_urls = [
    path('api/files/', include('src.apps.files.urls')),
]

if APP_TYPE == APP_TYPE_AUTH:
    urlpatterns = auth_urls + swagger_urls

if APP_TYPE == APP_TYPE_FILE:
    urlpatterns = file_urls + swagger_urls

if ENVIRONMENT == 'testing':
    urlpatterns = auth_urls + file_urls
