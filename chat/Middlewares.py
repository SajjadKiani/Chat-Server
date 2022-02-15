from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from chat.models import User


class TokenAuthMiddleware(BaseMiddleware):
    @database_sync_to_async
    def get_user(self, token):
        try:
            return Token.objects.get(key=token).user
        except Exception as _:
            return AnonymousUser()

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, r, s, **kwargs):
        token_key = None
        try:
            for header in scope['headers']:
                if header[0] == b'authentication':
                    token_key = header[1].decode().split()[-1]
                    break
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await self.get_user(token_key)
        return await super().__call__(scope, r, s)
