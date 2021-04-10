import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, UserRoom, Message, User
from django.utils import timezone
import pdb


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        try:
            await self.accept()
            self.room_group_name = self.scope['url_route']['kwargs']['room_name']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            raise

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            author = text_data_json['author']
            timestamp_raw = timezone.localtime(timezone.now())
            date_format = '%H:%M'
            timestamp = timezone.datetime.strftime(timestamp_raw, date_format)
            message = text_data_json['message']
            await self.createMessage(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'author': author,
                    'message': message,
                    'created_at': str(timestamp),
                }
            )
        except Exception as e:
            raise

    async def chat_message(self, event):
        try:
            author = event['author']
            message = event['message']
            created_at = event['created_at']

            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'author': author,
                'message': message,
                'created_at': created_at,
            }))
        except Exception as e:
            raise

    @database_sync_to_async
    def createMessage(self, event):
        try:
            room = Room.objects.get(id=self.room_group_name)
            user = User.objects.get(username=event['author'])
            Message.objects.create(
                user=user,
                room=room,
                message=event['message'],
            )
        except Exception as e:
            raise
