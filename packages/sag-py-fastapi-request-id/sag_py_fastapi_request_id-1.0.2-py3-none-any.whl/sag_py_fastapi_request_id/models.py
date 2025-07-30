from logging import LogRecord


class RequestIdLogRecord(LogRecord):
    request_id: str
