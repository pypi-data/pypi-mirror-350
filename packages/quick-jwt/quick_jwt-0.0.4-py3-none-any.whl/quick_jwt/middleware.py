from fastapi import Request
from starlette.types import ASGIApp, Scope, Receive, Send

from quick_jwt.config import QuickJWTConfig


class QuickJWTMiddleware:
    __slots__ = (
        'app',
        'config',
    )

    def __init__(self, app: ASGIApp, config: QuickJWTConfig):
        self.app = app
        if isinstance(config, QuickJWTConfig) is False:
            raise Exception("""Invalid type "config" param in QuickJWTMiddleware""")
        self.config = config

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] in ('http',):
            request = Request(scope, receive)
            request.state.quick_jwt_config = self.config
            scope['request'] = request

        await self.app(scope, receive, send)
