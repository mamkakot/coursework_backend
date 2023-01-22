from rest_framework import generics, authentication, status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView

from .models import Family
from .serializers import *


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_queryset(self):
        queryset = Room.objects.all()
        family = self.request.query_params.get('family')
        if family is not None:
            queryset = queryset.filter(family_id=family)

        return queryset


class SlaveViewSet(viewsets.ModelViewSet):
    queryset = Slave.objects.all()
    serializer_class = SlaveSerializer


class ChoreViewSet(viewsets.ModelViewSet):
    serializer_class = ChoreSerializer

    def get_queryset(self):
        queryset = Chore.objects.all()
        room = self.request.query_params.get('room')
        print(room)
        if room is not None:
            queryset = queryset.filter(room_id=room)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialInviteSerializer

    def get_queryset(self):
        queryset = Invite.objects.all()
        receiver_id = self.request.query_params.get("receiver")
        if receiver_id is not None:
            queryset = queryset.filter(receiver=receiver_id)  # .distinct("sender")
        return queryset

    def post(self, request):
        pass


class GetInvites(generics.ListAPIView):
    serializer_class = SpecialInviteSerializer

    def get_queryset(self):
        queryset = Invite.objects.all()
        receiver_id = self.request.query_params.get("receiver")
        if receiver_id is not None:
            queryset = queryset.filter(receiver=receiver_id)  # .distinct("sender")
        return queryset


class CreateInvite(APIView):
    serializer_class = SpecialInviteSerializer

    def post(self, request):
        sender_user = int(request.data.get("sender"))
        sender = Slave.objects.get(user_id__exact=sender_user).id
        print(f"sender {sender}")
        receiver_username = request.data.get("receiver")
        receiver = User.objects.get(username=receiver_username).id
        serializer = InviteSerializer(data={"sender": sender, "receiver": receiver})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
