from rest_framework import serializers

from .models import Chore, Room, Invite, Slave, Family
from django.contrib.auth.models import User
from django.db.models import Count


class ChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chore
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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

#
#
# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#
#         return user
