from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from api.modules.users.serializers import UserUpdateSerializer
from django.db.utils import IntegrityError

class UsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            users_data = serializer.data
            print(users)

            users_data = [{
                'username': user_data["username"],
                'admin': user_data["admin"]
            } for user_data in users_data ]

            return Response(data=users_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserOrganizerView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            user_data = {
                'username': user.username,
                'admin': user.admin
            }

            return Response(data=user_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
            if 'admin' in request.data:
                admin_value = request.data['admin'].lower()

                if admin_value == 'true':
                    user.admin = True
                elif admin_value == 'false':
                    user.admin = False
                else:
                    return Response({'error': 'Invalid admin value. Must be "true" or "false".'}, status=status.HTTP_400_BAD_REQUEST)

                user.save()

                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No admin data provided'}, status=status.HTTP_400_BAD_REQUEST)
        

        except ObjectDoesNotExist as e:
            print("e1")
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            print("e2")
            return Response(data={'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print("e3")
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            user_data = {
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'country': user.country,
                'photo': user.photo,
            }
            print("aici0")

            if user.photo:
                user_data['photo'] = request.build_absolute_uri(user.photo.url)
            else:
                user_data['photo'] = None

            return Response(data=user_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print("aici1")
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("aici2")
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
            if user != request.user:
                return Response(
                    data={
                        "errors":
                        "You can only update your own data"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            payload = {
                'username': request.data.get('username', user.username),
                'email': request.data.get('email', user.email),
                'phone': request.data.get('phone', user.phone),
                'country': request.data.get('country', user.country),
                'admin': request.data.get('admin', False),
                'photo': request.data.get('photo', user.photo)
            }

            print(payload)

            serializer = UserUpdateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)

            user.username = serializer.validated_data["username"]
            user.email = serializer.validated_data["email"]
            user.phone = serializer.validated_data["phone"]
            user.country = serializer.validated_data["country"]
            user.admin = serializer.validated_data["admin"]
            user.photo = serializer.validated_data["photo"]

            user.save()
            serializer = UserSerializer(user)
            user_data = serializer.data


            return Response(data=user_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            print("e1")
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            print("e2")
            return Response(data={'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print("e3")
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        