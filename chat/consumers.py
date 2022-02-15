import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from chat import REDIS


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        REDIS.Red.put(self)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        for x in REDIS.Red.data:
            await x.send(text_data=text_data)
