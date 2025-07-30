from typing import Any

from pytest import MonkeyPatch

from sag_py_logging.log_config_initializer import init_logging
from sag_py_logging.log_config_loader import LogLoader
from sag_py_logging.log_config_processors import LogProcessor


class TestLogProcessorOne(LogProcessor):
    def __call__(self, log_template: str) -> str:
        return f"{log_template}-LogProcessorOne"


class TestLogProcessorTwo(LogProcessor):
    def __call__(self, log_template: str) -> str:
        return f"{log_template}-LogProcessorTwo"


class TestLogLoader(LogLoader):
    def __call__(self, string_config: str) -> dict[str, Any]:
        return {"result": string_config}


def _get_config_file_content_mock(config_file: str, encoding: str) -> str:
    return "myFileContent"


def _init_python_logging_mock(log_config_dict: dict[str, Any]) -> None:
    pass


def test__init_logging(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("sag_py_logging.log_config_initializer._get_config_file_content", _get_config_file_content_mock)
    monkeypatch.setattr("sag_py_logging.log_config_initializer._init_python_logging", _init_python_logging_mock)

    # Act
    actual: dict[str, Any] = init_logging(
        "myconfig.json", TestLogLoader(), processors=[TestLogProcessorOne(), TestLogProcessorTwo()]
    )

    # Assert
    assert actual["result"] == "myFileContent-LogProcessorOne-LogProcessorTwo"


def test__init_logging__without_processors(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("sag_py_logging.log_config_initializer._get_config_file_content", _get_config_file_content_mock)
    monkeypatch.setattr("sag_py_logging.log_config_initializer._init_python_logging", _init_python_logging_mock)

    # Act
    actual: dict[str, Any] = init_logging("myconfig.json", TestLogLoader())

    # Assert
    assert actual["result"] == "myFileContent"
