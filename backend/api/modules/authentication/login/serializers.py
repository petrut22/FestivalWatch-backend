from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()
