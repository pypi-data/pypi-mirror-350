from abc import abstractmethod
from typing import Mapping


class LogProcessor:
    @abstractmethod
    def __call__(self, log_template: str) -> str:
        pass  # pragma: no cover


class FormatProcessor(LogProcessor):
    def __init__(self, placeholder_container: Mapping[str, object]) -> None:
        from string import Template

        self.template = Template
        self.placeholder_container: Mapping[str, object] = placeholder_container

    def __call__(self, log_template: str) -> str:
        return self.template(log_template).substitute(self.placeholder_container)


class JinjaProcessor(LogProcessor):
    def __init__(self, placeholder_container: Mapping[str, object]) -> None:
        try:
            import jinja2
        except ImportError as e:
            raise ModuleNotFoundError(
                "Module 'jinja2' not installed.  Please run " "'python -m pip install sag-py-logging[jinja]'"
            ) from e

        self.jinja = jinja2
        self.placeholder_container: Mapping[str, object] = placeholder_container

    def __call__(self, log_template: str) -> str:
        template = self.jinja.Template(log_template)
        return template.render(self.placeholder_container)
