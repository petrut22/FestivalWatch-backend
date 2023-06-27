import re
from rest_framework import serializers
from api.modules.users.models import User
from api.modules.festivals.models import Festival
from .models import Ticket

class FestivalSerializerPerFestival(serializers.ModelSerializer):

    class Meta:
        model = Festival
        fields = [
            'festival_name',
            'price'
        ]

class UserSerializerPerFestival(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username'
        ]

class TicketSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField(required=True, allow_null=False)
    festival = FestivalSerializerPerFestival(read_only=True)
    user = UserSerializerPerFestival(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'qr_code',
            'festival',
            'user',
        ]
