from contextvars import ContextVar

request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str:
    return request_id.get(None) or ""


def set_request_id(request_id_to_set: str) -> None:
    request_id.set(request_id_to_set)
