import uuid

from starlette.applications import Starlette
from starlette.types import Receive, Scope, Send

from .request_context import set_request_id as set_request_id_to_context


class RequestContextMiddleware:
    def __init__(self, app: Starlette) -> None:
        self.app: Starlette = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self._set_request_id(scope)
        await self.app(scope, receive, send)
        return

    def _set_request_id(self, scope: Scope) -> None:
        if scope["type"] in ["http", "websocket"]:
            request_id = str(uuid.uuid4().hex)
            set_request_id_to_context(request_id)
