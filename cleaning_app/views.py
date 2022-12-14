from rest_framework import generics, authentication
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView

from .serializers import *


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         print('list')
    #         return RoomSerializer
    #     if self.action == 'retrieve':
    #         print('retr')
    #         return RoomDetailsSerializer
    # return RoomSerializer


class ChoreViewSet(viewsets.ModelViewSet):
    # queryset = Chore.objects.all()
    serializer_class = ChoreSerializer

    def get_queryset(self):
        queryset = Chore.objects.all()
        room = self.request.query_params.get('room')
        if room is not None:
            queryset = queryset.filter(room_id=room)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
