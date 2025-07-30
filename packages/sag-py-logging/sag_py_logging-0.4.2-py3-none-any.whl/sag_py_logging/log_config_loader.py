from abc import abstractmethod
from typing import Any


class LogLoader:
    @abstractmethod
    def __call__(self, log_template: str) -> dict[str, Any]:
        pass  # pragma: no cover


class JsonLoader(LogLoader):
    def __init__(self) -> None:
        import json

        self.json = json

    def __call__(self, string_config: str) -> dict[str, Any]:
        return self.json.loads(string_config)


class TomlLoader(LogLoader):
    def __init__(self) -> None:
        try:
            import tomli

            self.tomli = tomli
        except ImportError as e:
            raise ModuleNotFoundError(
                "Module 'tomli' not installed.  Please run 'python -m pip install sag-py-logging[toml]'"
            ) from e

    def __call__(self, string_config: str) -> dict[str, Any]:
        return self.tomli.loads(string_config)
