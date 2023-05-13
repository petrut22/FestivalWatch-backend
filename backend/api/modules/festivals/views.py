from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FestivalSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import IntegrityError
from .models import Festival


class FestivalsView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        try:
            festivals = Festival.objects.all()
            serializer = FestivalSerializer(festivals, many=True)

            festivals_data = serializer.data
            print(festivals)
            festivals_data = [{
                'id': festival_data["id"],
                'festival_name': festival_data["festival_name"],
                'date': festival_data["date"],
                'time': festival_data["time"],
                'location_lat': festival_data["location_lat"],
                'location_lon': festival_data["location_lon"],
                'location_address': festival_data["location_address"],
                'photo_cover': request.build_absolute_uri(festival_data["photo_cover"]),
                'photo_description': request.build_absolute_uri(festival_data["photo_description"]),
                'festival_admin': {
                    **festival_data["festival_admin"],
                },
                'description': festival_data["description"],
            } for festival_data in festivals_data ]

            return Response(data=festivals_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            payload = {
                "festival_name": request.data.get("festival_name", None),
                "date": request.data.get("date", None),
                "time": request.data.get("time", None),
                "location_lat": request.data.get("location_lat", None),
                "location_lon": request.data.get("location_lon", None),
                "location_address": request.data.get("location_address", None),
                "photo_cover": request.data.get("photo_cover", None),
                "photo_description": request.data.get("photo_description", None),
                "description": request.data.get("description", None),
            }

            if not request.user:
                return Response(data={'errors': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)


            serializer = FestivalSerializer(data=payload)
            if serializer.is_valid():
                festival = Festival(**serializer.validated_data)
                festival.festival_admin = request.user
                festival.save()

                serializer = FestivalSerializer(festival)

                festival_data = serializer.data

                festival_data = {
                    'id': festival_data["id"],
                    'festival_name': festival_data["festival_name"],
                    'date': festival_data["date"],
                    'time': festival_data["time"],
                    'location_lat': festival_data["location_lat"],
                    'location_lon': festival_data["location_lon"],
                    'location_address': festival_data["location_address"],
                    'photo_cover': festival_data["photo_cover"],
                    'photo_description': festival_data["photo_description"],
                    'festival_admin': {
                        **festival_data["festival_admin"],
                    },
                    'description': festival_data["description"],
                }

                return Response(data=festival_data, status=status.HTTP_201_CREATED)
            return Response(data={'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            festivals = Festival.objects.all()
            festivals.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FestivalView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, pk):
        try:
            festival = Festival.objects.get(pk=pk)
            serializer = FestivalSerializer(festival)

            festival_data = serializer.data

            festival_data = {
                'id': festival_data["id"],
                'festival_name': festival_data["festival_name"],
                'date': festival_data["date"],
                'time': festival_data["time"],
                'location_lat': festival_data["location_lat"],
                'location_lon': festival_data["location_lon"],
                'location_address': festival_data["location_address"],
                'photo_cover': festival_data["photo_cover"],
                'photo_description': festival_data["photo_description"],
                'festival_admin': {
                    **festival_data["festival_admin"],
                },
                'description': festival_data["description"],
            }


            return Response(data=festival_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):
        try:
            festival = Festival.objects.get(pk=pk)
            print("salut")
            payload = {
                "festival_name": request.data.get("festival_name", festival.festival_name),
                "date": request.data.get("date", festival.date),
                "time": request.data.get("time", festival.time),
                "location_lat": request.data.get("location_lat", festival.location_lat),
                "location_lon": request.data.get("location_lon", festival.location_lon),
                "location_address": request.data.get("location_address", festival.location_address),
                "photo_cover": request.data.get("photo_cover", festival.photo_cover),
                "photo_description": request.data.get("photo_description", festival.photo_description),
                "description": request.data.get("description", festival.description),
            }

            serializer = FestivalSerializer(festival, data=payload)

            if serializer.is_valid():
                serializer.save()

                festival_data = serializer.data
                festival_data = {
                    'id': festival_data["id"],
                    'festival_name': festival_data["festival_name"],
                    'date': festival_data["date"],
                    'time': festival_data["time"],
                    'location_lat': festival_data["location_lat"],
                    'location_lon': festival_data["location_lon"],
                    'location_address': festival_data["location_address"],
                    'photo_cover': festival_data["photo_cover"],
                    'photo_description': festival_data["photo_description"],
                    'festival_admin': {
                        **festival_data["festival_admin"],
                    },
                    'description': festival_data["description"],
                }

                print(festival_data)

                return Response(data=festival_data, status=status.HTTP_200_OK)
            
            return Response(data={'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def delete(self, request, pk):
        try:
            festival = Festival.objects.get(pk=pk)
            festival.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 