from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from appChat.models import Room, ChatHistory
from appAuth.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Room.objects.all())])

    class Meta:
        model = Room
        fields = ["name", "participants"]


class ChatHistorySerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)

    class Meta:
        model = ChatHistory
        fields = ["created_at", "owner", "room", "message", "to"]
        read_only_fields = ["created_at", "owner", "room", "message", "to"]
