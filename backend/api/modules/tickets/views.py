from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer
from .models import User
from .models import Festival
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import IntegrityError
from .models import Ticket


class TicketsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            tickets_data = serializer.data
            tickets_data = [{
                'qr_code': ticket_data["qr_code"],
                'user': {
                    **ticket_data["user"],
                },
                'festival': {
                    **ticket_data["festival"],
                }
            } for ticket_data in tickets_data ]

            return Response(data=tickets_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            tickets = Ticket.objects.all()
            tickets.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            payload = {
                "qr_code": request.data.get("qr_code", None),
                "festival_name": request.data.get("festival_name", None)
            }

            if not request.user:
                return Response(data={'errors': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)

            serializer = TicketSerializer(data=payload)
            if serializer.is_valid():
                ticket = Ticket(**serializer.validated_data)
                festival_name = payload["festival_name"]
                ticket.user= request.user
                ticket.festival= Festival.objects.get(festival_name=festival_name)
                ticket.save()

                serializer = TicketSerializer(ticket)

                ticket_data = serializer.data

                ticket_data = {
                    'qr_code': ticket_data["qr_code"],
                    'festival': {
                        **ticket_data["festival"],
                    },
                    'user': {
                        **ticket_data["user"],
                    },
                }
                return Response(data=ticket_data, status=status.HTTP_201_CREATED)
            return Response(data={'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class TicketView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, user_name, festival_name):
        try:
            user = User.objects.get(username=user_name)
            festival = Festival.objects.get(festival_name=festival_name)

            ticket = Ticket.objects.get(user=user, festival=festival)
            serializer = TicketSerializer(ticket)
            ticket_data = serializer.data


            ticket_data = {
                'qr_code': ticket_data["qr_code"],
                'festival': {
                    **ticket_data["festival"],
                },
                'user': {
                    **ticket_data["user"],
                },
            }


            return Response(data=ticket_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
