from django.conf.urls import url

from src.accounts.api.views.login_view import UserLoginView
from src.accounts.api.views.register_views import UserRegistrationView
from src.accounts.api.views.refresh_view import RefreshView

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^login', UserLoginView.as_view()),
    url(r'^refresh', RefreshView.as_view()),
]
