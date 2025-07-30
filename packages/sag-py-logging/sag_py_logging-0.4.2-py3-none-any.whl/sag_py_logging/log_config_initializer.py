import logging
import logging.config
from typing import Any

from sag_py_logging.log_config_loader import LogLoader
from sag_py_logging.log_config_processors import LogProcessor


def init_logging(
    config_file: str, loader: LogLoader, encoding: str = "UTF-8", processors: list[LogProcessor] | None = None
) -> dict[str, Any]:
    config_template: str = _get_config_file_content(config_file, encoding)
    parsed_template: str = _parse_template(processors, config_template)
    log_config: dict[str, Any] = loader(parsed_template)
    _init_python_logging(log_config)
    return log_config


def _get_config_file_content(config_file: str, encoding: str) -> str:
    with open(config_file, "r", encoding=encoding) as log_config_reader:
        return log_config_reader.read()


def _parse_template(processors: list[LogProcessor] | None, config_template: str) -> str:
    parsed_template: str = config_template
    if processors:
        for processor in processors:
            parsed_template = processor(parsed_template)
    return parsed_template


def _init_python_logging(log_config_dict: dict[str, Any]) -> None:
    logging.basicConfig()
    logging.config.dictConfig(log_config_dict)
