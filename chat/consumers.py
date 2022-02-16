import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat import REDIS
from chat.models import Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # TODO: Handle unauthorized user
        try:
            REDIS.BankOfReds.consumers[self.scope['user'].username] = self
        except Exception as _:
            print("fuck")
        print(REDIS.BankOfReds.consumers.keys())
        await self.accept()

    async def disconnect(self, close_code):
        pass
        # del REDIS.BankOfReds.consumers[self.scope['user'].username]
        # del REDIS.BankOfReds.whichPV[self.scope['user'].username]

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        operation = text_data_json['operation']
        if operation == 'chat':
            REDIS.BankOfReds.whichPV[self.scope['user'].username] = text_data_json['data']
        elif operation == 'send':
            sender = self.scope['user']

            receiver = REDIS.BankOfReds.whichPV[sender.username]
            receiver_consumer = REDIS.BankOfReds.consumers.get(receiver, None)

            print(REDIS.BankOfReds.consumers.keys())
            # TODO: Sync to async
            rec = await sync_to_async(User.objects.get)(
                username=receiver
            )
            message = await sync_to_async(Message.objects.create)(text=text_data_json['data'],
                                                                  sender=sender,
                                                                  receiver=rec)
            if receiver_consumer is not None:
                await receiver_consumer.send(text_data=json.dumps(message.to_json()))
            else:
                print("consumer nulle")
            print(message.to_json())
