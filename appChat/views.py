import secrets

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from appChat.serializers import RoomSerializer, ChatHistorySerializer
from appChat.models import Room, ChatHistory


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Room.objects.filter(participants__pk=user.id)
        return queryset

    @action(methods=['get'], detail=False,
            url_path='generate-token', url_name='generate_token')
    def generate_token(self, request):
        # objects.get_or_create
        hash_str = secrets.token_hex(nbytes=32)

        return Response({"message": hash_str})


class ChatHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_name = self.request.query_params.get('room_name')

        return ChatHistory.objects.filter(room__name=room_name)

    def get_serializer_class(self):
        self.http_method_names = ["get"]
        return ChatHistorySerializer
