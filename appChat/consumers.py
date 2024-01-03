import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from appAuth.models import User
from appChat.models import ChatHistory, Room

from appChat.openai_utils import send_to_openai


@database_sync_to_async
def add_room(room_name, participants):
    if room_name:
        room, created = Room.objects.get_or_create(name=room_name)
        if created:
            room.participants.set(participants)
            room.name = room_name
            room.save()
    else:
        room, created = Room.objects.get_or_create(
            participants=participants, name=room_name
        )
    return str(room.pk), created


@database_sync_to_async
def get_user(pk):
    user = User.objects.get(pk=pk)
    return user


@database_sync_to_async
def save_messages(from_user, to_user, room_id, message):
    room = Room.objects.get(pk=room_id)
    to_user = User.objects.get(pk=to_user)

    # create new history item
    history = ChatHistory.objects.create(
        message=message,
        owner=from_user,
        to=to_user,
        room=room,
    )

    return str(history.pk)


class SocketConsumer(AsyncJsonWebsocketConsumer):
    """
    Websocket class that handles web socket connection and traffic.
    """

    async def connect(self):
        """
        Verifies the users access and connects to the websocket.
        """
        try:
            # gets user from scope
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # TODO verificar autenticação
            user_id = str(self.scope['query_string']).split('=')[1].replace("'", "")
            user_id = int(user_id)
            self.user = await get_user(user_id)

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
        except Exception as e:
            print(e)
            await self.close()

    async def receive_json(self, content):
        try:
            message = content['message']
            fromId = content['fromId']
            toId = content['toId']

            participants = [fromId, toId]

            room_id, created = await add_room(
                room_name=self.room_name, participants=participants
            )

            if created or room_id:
                await save_messages(
                    self.user, toId, room_id, message
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'toId': toId,
                        'fromId': fromId,
                    }
                )

                # SENDS THE RECEIVED MESSAGE TO OPENAI
                resp = send_to_openai(message)
                resp_from_gpt = resp.choices[0].text

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': resp_from_gpt,
                        'toId': fromId,
                        'fromId': toId,
                    }
                )

        except Exception as e:
            print(e)
            await self.close()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def note_message(self, event):
        """
        Transmit notification message to room
        """
        message = {
            "message_type": "notification",
            "room": event["room"],
            "message": event["message"],
        }
        await self.send_json(message)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def add_message(self, event):
        await self.send_json(event)
