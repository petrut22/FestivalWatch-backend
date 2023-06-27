import re
from api.modules.users.models import User
from api.modules.users.serializers import UserSerializer
from rest_framework import serializers
from .models import Festival

class UserSerializerPerFestival(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'username',
            'phone',
            'country'
        ]

class FestivalSerializer(serializers.ModelSerializer):
    festival_admin = UserSerializerPerFestival(read_only=True)
    photo_cover = serializers.ImageField(required=False, allow_null=True)
    photo_description = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Festival
        fields = [
            'id',
            'photo_cover',
            'photo_description',
            'time',
            'date',
            'location_lat',
            'location_lon',
            'location_address',
            'festival_name',
            'description',
            'festival_admin',
            'price',

        ]
