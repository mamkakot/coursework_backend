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


class GetUserFamily(APIView):
    def get(self, request):
        user_id = request.query_params.get("user")
        family = Slave.objects.get(user_id=user_id).family.id
        return Response(family)


class ChoreViewSet(viewsets.ModelViewSet):
    serializer_class = ChoreSerializer

    def get_queryset(self):
        queryset = Chore.objects.all()
        room = self.request.query_params.get('room')
        print(room)
        if room is not None:
            queryset = queryset.filter(room_id=room)

        return queryset


class CreateUserView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FamilySlaves(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        serializer = UserSerializer
        family_id = self.request.query_params.get("family")
        if family_id is not None:
            queryset = User.objects.all().filter(slave__family_id=family_id)
            return queryset
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()


class FamilyView(APIView):
    def post(self, request):
        user_id = self.request.query_params.get("user")
        family = FamilySerializer(data=request.data)
        if family.is_valid():
            family.save()

            slave = Slave.objects.get(user_id=user_id)
            print(slave)
            slave.family_id = family.data['id']
            slave.is_admin = True
            slave.save()
            return Response(family.data)
        return Response(family.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = self.request.query_params.get("user")
        disband = self.request.query_params.get("disband")
        slave = Slave.objects.get(user_id=user_id)
        slave_serializer = SlaveSerializer(slave)
        if slave is not None:
            slave.family_id = None
            if disband:
                slave.is_admin = False
            else:
                slave.is_admin = None
            slave.save()
            return Response(slave_serializer.data)
        return Response(slave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialInviteSerializer

    def get_queryset(self):
        queryset = Invite.objects.all()
        receiver_id = self.request.query_params.get("receiver")
        if receiver_id is not None:
            queryset = queryset.filter(receiver=receiver_id).distinct("sender")
        return queryset

    def post(self, request):
        pass


class GetInvites(generics.ListAPIView):
    serializer_class = SpecialInviteSerializer

    def get_queryset(self):
        queryset = Invite.objects.all().distinct('sender__user_id', 'receiver', 'is_join_request')
        receiver_id = self.request.query_params.get("receiver")
        # queryset = queryset.filter(sender__user_id=[item['sender'] for item in distinct])

        if receiver_id is not None:
            queryset = queryset.filter(receiver=receiver_id)

        return queryset


class CreateInvite(APIView):
    serializer_class = SpecialInviteSerializer

    def post(self, request):
        receiver_username = request.data.get("receiver")
        sender_user = int(request.data.get("sender"))
        receiver = Slave.objects.get(user__username=receiver_username).id
        sender = Slave.objects.get(user_id__exact=sender_user).id
        if receiver != sender:
            print(f"sender {sender}")
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
