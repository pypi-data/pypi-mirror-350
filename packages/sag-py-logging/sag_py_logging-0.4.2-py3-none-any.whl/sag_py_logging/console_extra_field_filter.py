import contextlib
import json
import logging
from typing import Any


class ConsoleExtraFieldFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name=name)
        self.excluded_standard_fields: set[str] = {
            "@metadata",
            "args",
            "asctime",
            "color_message",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "id",
            "levelname",
            "levelno",
            "lineno",
            "logsource",
            "message",
            "module",
            "msecs",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "program",
            "relativeCreated",
            "stack_info",
            "stringified_extra",
            "tags",
            "taskName",
            "thread",
            "threadName",
            "type",
        }

    def filter(self, record: logging.LogRecord) -> bool:
        extra_fields: dict[str, Any] = self._get_extra_fields(record)
        extra_list: list[str] = self._to_key_value_strings(extra_fields)
        record.stringified_extra = ", ".join(extra_list)
        return True

    def _get_extra_fields(self, record: logging.LogRecord) -> dict[str, Any]:
        return {key: value for key, value in record.__dict__.items() if key not in self.excluded_standard_fields}

    def _to_key_value_strings(self, extra_fields: dict[str, Any]) -> list[str]:
        return [f"{key}={self._generate_string_value(value)}" for key, value in extra_fields.items()]

    def _generate_string_value(self, value: Any) -> str:
        with contextlib.suppress(Exception):
            return json.dumps(value)

        with contextlib.suppress(Exception):
            return json.dumps(value.__dict__)

        return str(value)
