from django.urls import path, include

urlpatterns = [
    path('api/users/', include('src.apps.accounts.urls')),
    path('api/files/', include('src.apps.files.urls')),
]
