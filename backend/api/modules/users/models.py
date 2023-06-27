from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=10, null=True)
    country = models.CharField(null=True, max_length=50)
    admin = models.BooleanField(default=False, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    

    # used for the Admin view in Django
    def __str__(self):
        return self.username
    
    class Meta:
        # used for the Admin view in Django
        verbose_name_plural = "Users"