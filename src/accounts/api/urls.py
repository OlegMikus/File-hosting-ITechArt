from django.urls import path

from src.accounts.api.views.login import UserLoginView
from src.accounts.api.views.signup import UserSignUpView
from src.accounts.api.views.refresh import RefreshView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]
