from logging import Filter, LogRecord

from .request_context import get_request_id


class RequestContextLoggingFilter(Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name=name)

    def filter(self, record: LogRecord) -> bool:
        if request_id := get_request_id():
            record.request_id = request_id

        return True
