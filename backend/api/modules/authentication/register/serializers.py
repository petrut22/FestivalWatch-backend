import re
from rest_framework import serializers
import pycountry

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_null=False)
    username = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False)
    phone = serializers.CharField(required=True, allow_null=False)
    country = serializers.CharField(required=True, allow_null=False)

    def validate_email(self, value):
        if not re.match(r'.+?@.+?\..+', value):
            raise serializers.ValidationError('Invalid email!')

        return value
    
    def validate_username(self, value):
        if not len(value) > 0:
            raise serializers.ValidationError('Invalid empty username!')

        if not re.match(r'^[a-zA-Z0-9\_\-\.]+$', value):
            raise serializers.ValidationError('Invalid username! Only a-z A-Z 0-9 _-. characters allowed')

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Pasword is too short, at least 8 characters are required!')

        return value

    def validate_phone(self, value):
        if not len(value) == 10:
            raise serializers.ValidationError('Incomplete phone number format!')
        
        if not re.match(r'^[0-9\_\-\.]+$', value):
            raise serializers.ValidationError('Invalid phone number format!')

        return value

    def validate_country(self, value):

        if not re.match(r'^[a-zA-Z\-\.]', value):
            raise serializers.ValidationError('Invalid country! Only a-z A-Z -. characters allowed')

        country_names = [country.name for country in pycountry.countries]
        if not value in country_names:
            raise serializers.ValidationError('Invalid country! Introduce a valid country')

        return value