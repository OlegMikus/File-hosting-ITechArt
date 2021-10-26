from django.urls import path, include

urlpatterns = [
    path('api/users/', include('src.accounts.api.urls')),
    path('api/files/', include('src.files.api.urls')),
]
