from django.urls import re_path, path
from .views import FestivalView
from .views import FestivalsView

app_name = 'festivals'

urlpatterns = [
    path('', FestivalsView.as_view(), name='festivalsView'),
    re_path('(?P<pk>[0-9]+)/?$', FestivalView.as_view(), name='festivalView'),
]
