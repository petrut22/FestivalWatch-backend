from django.urls import re_path, path
from .views import TicketView
from .views import TicketsView

app_name = 'tickets'

urlpatterns = [
    path('', TicketsView.as_view(), name='ticketsView'),
    re_path('(?P<user_name>[a-zA-Z0-9\_\-\.]+)/(?P<festival_name>[a-zA-Z0-9\_\-\.]+)/$', TicketView.as_view(), name='ticketView'),
]
