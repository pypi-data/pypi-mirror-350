from logging import LogRecord


class ExtraFieldsLogRecord(LogRecord):
    stringified_extra: str
