from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class LoginView(APIView):
    permission_classes = ()

    def get(self, request):
        return Response(data={'msg': 'test'}, status=status.HTTP_200_OK)

    def post(self, request):
        payload = {
            'email_username': request.data.get('email_username'),
            'password': request.data.get('password'),
        }   
        serializer = LoginSerializer(data=payload)
        try:
            serializer.is_valid(raise_exception=True)
            print("aici0")
            user = authenticate(username=serializer.data['email_username'], password=serializer.data['password'])
            print("aici01")
            if not user:
                print("aici02")
                return Response(data={'error': 'User not found!'}, status=status.HTTP_401_UNAUTHORIZED)
            print("aici1")
            token, _ = Token.objects.get_or_create(user=user)
            print("aici2")
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            print("aiciE1")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("aiciE2")
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()

        return Response(data={'msg': 'Successfuly logged out!'}, status=status.HTTP_200_OK)

class ValidateTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
