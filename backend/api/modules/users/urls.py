from django.urls import re_path, path
from .views import UserView, UsersView, UserOrganizerView

app_name = 'users'
 
urlpatterns = [
    path('', UsersView.as_view(), name='usersView'),
    re_path('organizer/(?P<username>[a-zA-Z0-9\_\-\.]+)/?$', UserOrganizerView.as_view(), name='userOrganizerView'),
    re_path('user/(?P<username>[a-zA-Z0-9\_\-\.]+)/?$', UserView.as_view(), name='userView'),
]
