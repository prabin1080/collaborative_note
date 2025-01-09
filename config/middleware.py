from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode())
        token_key = query_params.get("token")

        if token_key:
            user = await self.get_user(token_key[0])
            scope["user"] = user
        
        return await super().__call__(scope, receive, send)
    
    @database_sync_to_async
    def get_user(self, token_key):
        try:
            return Token.objects.get(key=token_key).user
        except Token.DoesNotExist:
            return AnonymousUser()
