from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('src.accounts.api.urls')),
    path('api/files/', include('src.files.api.urls'))
]
