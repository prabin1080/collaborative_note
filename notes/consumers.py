import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Note
from asgiref.sync import sync_to_async

from config.clients import redis_client

class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        self.room_group_name = f"note_{self.note_id}"
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            await sync_to_async(redis_client.sadd)(f"online_users:{self.note_id}", self.user.username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.broadcast_online_users()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await sync_to_async(redis_client.srem)(f"online_users:{self.note_id}", self.user.username)

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.broadcast_online_users()

    async def broadcast_online_users(self):
        users = await sync_to_async(redis_client.smembers)(f"online_users:{self.note_id}")
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_list_update", "users": list(users)}
        )

    async def user_list_update(self, event):
        await self.send(text_data=json.dumps({"type": "user_list", "users": event["users"]}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data["content"]

        # Save to database
        await self.save_note_content(content)

        # Broadcast to all connected users
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "note_update",
                "content": content,
            }
        )

    async def note_update(self, event):
        await self.send(text_data=json.dumps({"content": event["content"]}))

    @sync_to_async
    def save_note_content(self, content):
        note = Note.objects.get(id=self.note_id)
        note.content = content
        note.save()
