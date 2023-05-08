from django.urls import re_path, path
from .views import UserView

app_name = 'users'

urlpatterns = [
    path('', UserView.as_view(), name='userView'),
    # re_path('self/change_password/?$', PlayerSelfChangePassword.as_view(), name='playerSelfChangePasswordView'),
    #re_path('self/?$', UserSelfView.as_view(), name='playerSelfView'),
    re_path('user/(?P<username>[a-zA-Z0-9\_\-\.]+)/?$', UserView.as_view(), name='userView'),
]
