from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
# from .utils import EXPERIENCE_REQUIRED_PER_LEVEL_PER_THRESHOLD, LEVEL_THRESHOLDS, \
#     get_level_lower_limit, get_level_upper_limit, get_level_from_experience
from django.db.models import Q
from api.modules.users.serializers import UserUpdateSerializer
from django.db.utils import IntegrityError

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
                'photo': request.data.get('photo', user.photo)
            }

            print(payload)

            serializer = UserUpdateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)

            user.username = serializer.validated_data["username"]
            user.email = serializer.validated_data["email"]
            user.phone = serializer.validated_data["phone"]
            user.country = serializer.validated_data["country"]
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


        # q_query = None
        # query_params = {}

        # if params["name"] is not None:
        #     q_query = Q(username__icontains=params["name"])
        #     q_query.add(Q(email__icontains=params["name"]), Q.OR)

        # # if params["level_from"] is not None and params["level_to"] is not None:
        # #     query_params.update({"experience__range": (get_level_lower_limit(int(params["level_from"])), get_level_upper_limit(int(params["level_to"])))})
        # # elif params["level_from"] is not None:
        # #     query_params.update({"experience__gte": get_level_lower_limit(int(params["level_from"]))})
        # # elif params["level_to"] is not None:
        # #     query_params.update({"experience__lte": get_level_upper_limit(int(params["level_to"]))})

        # users = User.objects.filter(**query_params)

        # if q_query is not None:
        #     users = users.filter(q_query)

        # serializer = UserSerializer(users, many=True)
        # users_data = serializer.data
        # # users_data = [{**player_data, 'level': get_level_from_experience(experience=player_data['experience'])} for player_data in players_data]

        # return Response(data=users_data, status=status.HTTP_200_OK)

# class PlayerView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, username):
#         try:
#             player = Player.objects.get(username=username)
#             serializer = UserSerializer(player)

#             player_data = {**serializer.data, 'level': get_level_from_experience(experience=serializer.data['experience'])}

#             return Response(data=player_data, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def put(self, request, username):
#         try:
#             player = Player.objects.get(username=username)

#             if player != request.user:
#                 return Response(
#                     data={
#                         "errors":
#                         "You can only update your own data"
#                     },
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             payload = {
#                 'username': request.data.get('username', player.username),
#                 'email': request.data.get('email', player.email),
#                 'first_name': request.data.get('first_name', player.first_name),
#                 'last_name': request.data.get('last_name', player.last_name),
#             }

#             serializer = UserUpdateSerializer(data=payload)
#             serializer.is_valid(raise_exception=True)

#             player.username = serializer.validated_data["username"]
#             player.email = serializer.validated_data["email"]
#             player.first_name = serializer.validated_data["first_name"]
#             player.last_name = serializer.validated_data["last_name"]

#             player.save()

#             serializer = UserSerializer(player)

#             player_data = {**serializer.data, 'level': get_level_from_experience(experience=serializer.data['experience'])}

#             return Response(data=player_data, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except IntegrityError as e:
#             return Response(data={'error': str(e)}, status=status.HTTP_409_CONFLICT)
#         except Exception as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def delete(self, request, username):
#         try:
#             player = Player.objects.get(username=username)

#             if player != request.user:
#                 return Response(
#                     data={
#                         "errors":
#                         "You can only delete your own account"
#                     },
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             player.delete()

#             return Response(data={}, status=status.HTTP_204_NO_CONTENT)
#         except ObjectDoesNotExist as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class PlayerSelfView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         player = request.user
#         serializer = UserSerializer(player)

#         player_data = serializer.data
#         player_data = {**player_data, 'level': get_level_from_experience(experience=player_data['experience'])}

#         return Response(data=player_data, status=status.HTTP_200_OK)

# class PlayerSelfChangePassword(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         try:
#             player = request.user

#             payload = {
#                 'password': request.data.get('password', None),
#             }

#             if payload["password"] is None:
#                 return Response(
#                     data={
#                         'errors':
#                         'No password was provided'
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             player.set_password(payload["password"])
#             player.save()
            
#             serializer = UserSerializer(player)

#             player_data = {**serializer.data, 'level': get_level_from_experience(experience=serializer.data['experience'])}

#             return Response(data=player_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data={'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
