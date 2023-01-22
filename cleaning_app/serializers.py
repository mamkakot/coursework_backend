from rest_framework import serializers

from .models import Chore, Room, Invite, Slave, Family
from django.contrib.auth.models import User
from django.db.models import Count
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


class ChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chore
        fields = '__all__'


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'username', 'password',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        print(user.username)
        Slave.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        Slave.objects.create(user=user)
        return user


class SpecialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SlaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = '__all__'


class SpecialSlaveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Slave
        fields = ['user']


class SpecialInviteSerializer(serializers.ModelSerializer):
    sender = SpecialSlaveSerializer(read_only=True, required=False)

    class Meta:
        model = Invite
        fields = "__all__"


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    sum_status = serializers.SerializerMethodField()
    count_chores = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    @staticmethod
    def get_sum_status(instance):
        try:
            status = int(len(Chore.objects.filter(room=instance, status=True)) /
                         Chore.objects.filter(room=instance).count() * 100)
        except ZeroDivisionError:
            status = None
        return status

    @staticmethod
    def get_count_chores(instance):
        return Chore.objects.filter(room=instance).count()


class RoomDetailsSerializer(serializers.ModelSerializer):
    rooms_chores = ChoreSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'rooms_chores']


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'
