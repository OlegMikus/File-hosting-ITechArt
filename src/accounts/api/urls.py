from django.conf.urls import url

from src.accounts.api.views.login_view import UserLoginView
from src.accounts.api.views.register_views import UserRegistrationView

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^login', UserLoginView.as_view()),
]
