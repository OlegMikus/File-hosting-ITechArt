from django.urls import path, include

urlpatterns = [
    path('api/users/', include('src.apps.accounts.api.urls')),
    path('api/files/', include('src.apps.files.api.urls')),
]
