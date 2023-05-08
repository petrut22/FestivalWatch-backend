from django.urls import re_path, path
from .register.views import RegisterView
from .login.views import LoginView, LogoutView, ValidateTokenView

app_name = 'auth'

urlpatterns = [
    re_path(r'register/?$', RegisterView.as_view(), name='registerView'),
    re_path(r'login/?$', LoginView.as_view(), name='loginView'),
    re_path(r'logout/?$', LogoutView.as_view(), name='logoutView'),
    re_path(r'validate/?$', ValidateTokenView.as_view(), name='validateTokenView'),
]