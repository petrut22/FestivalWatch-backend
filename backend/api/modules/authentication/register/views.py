from django.db.utils import IntegrityError
from api.modules.users.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = ()

    def get(self, request):
        return Response(data={'msg': 'test'}, status=status.HTTP_200_OK)

    def post(self, request):
        payload = {
            'email': request.data.get('email', None),
            'username': request.data.get('username', None),
            'password': request.data.get('password', None),
        }
    

        if not len(User.objects.all().filter(email=payload['email'])) == 0:
            return Response(data={'error': 'Conflict: email already exists!'}, status=status.HTTP_409_CONFLICT)
        
        if request.data.get('phone'):
            payload.update({'phone': request.data.get('phone')})
        if request.data.get('country'):
            payload.update({'country': request.data.get('country')})

        print(payload)


        serializer = RegisterSerializer(data=payload)

        print("1AICI")
        try:
            serializer.is_valid(raise_exception=True)
            print("2")
            User.objects.create_user(**serializer.data)
            print("3")
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

            if not user:
                return Response({'error': 'Something\'s ducked really badly'}, status=status.HTTP_418_IM_A_TEAPOT)
            token, _ = Token.objects.get_or_create(user=user)            
            return Response(data={'token': token.key}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            print("aici exceptie 1")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response(data={'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print(e)
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
