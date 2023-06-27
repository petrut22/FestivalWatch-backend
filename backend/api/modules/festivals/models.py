from django.db import models
from api.modules.users.models import User

TIME_FORMAT = "%Y-%m-%d"

class Festival(models.Model):
    festival_name = models.CharField(max_length=30, default='')
    date = models.CharField(max_length=60, default='')
    time = models.TimeField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    location_address = models.CharField(max_length=255, default='')
    photo_cover = models.ImageField(upload_to='festival_photos/', blank=True, null=True)
    photo_description = models.ImageField(upload_to='festival_photos/', blank=True, null=True)
    festival_admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='room_administrator')
    description = models.CharField(max_length=3000, default='')
    price = models.FloatField()


    

    # used for the Admin view in Django
    def __str__(self):
        return self.festival_name
    
    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Festivals"