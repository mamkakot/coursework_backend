from rest_framework import serializers

from .models import Chore, Room


class ChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chore
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    sum_status = serializers.SerializerMethodField()

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
