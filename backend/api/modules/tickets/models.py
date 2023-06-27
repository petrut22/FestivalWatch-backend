from django.db import models
from api.modules.users.models import User
from api.modules.festivals.models import Festival


class Ticket(models.Model):
    qr_code = models.CharField(max_length=3000, default='')
    festival = models.ForeignKey(Festival, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    # used for the Admin view in Django
    def __str__(self):
        return self.qr_code
    
    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Tickets"