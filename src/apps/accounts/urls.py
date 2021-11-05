from django.urls import path

from src.apps.accounts.views.change_password import ChangePasswordView
from src.apps.accounts.views.login import UserLoginView
from src.apps.accounts.views.profile import ProfileView
from src.apps.accounts.views.signup import UserSignUpView
from src.apps.accounts.views.refresh import RefreshView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password')
]
