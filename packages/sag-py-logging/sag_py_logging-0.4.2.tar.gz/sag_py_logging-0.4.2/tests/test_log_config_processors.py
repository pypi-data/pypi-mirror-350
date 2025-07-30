from typing import Mapping

import pytest

from sag_py_logging.log_config_processors import FormatProcessor, JinjaProcessor


@pytest.fixture(name="format_template")
def fixture_format_template() -> str:
    return """{
        "version": 1,
        "disable_existing_loggers": "true",
        "root": {
            "handlers": ["myhandler"],
            "level": "INFO"
        },
        "handlers": {
            "myhandler": {
                "host": "${host}",
                "port": ${port},
                "formatter": "handler_formatter"
            }
        }
    }"""


@pytest.fixture(name="jinja_template")
def fixture_jinja_template() -> str:
    return """{
        "version": 1,
        "disable_existing_loggers": "true",
        "root": {
            "handlers": ["myhandler"],
            "level": "INFO"
        },
        "handlers": {
            "myhandler": {
                "host": "{{host}}",
                "port": {{port}},
                "formatter": "handler_formatter"
            }
        }
    }"""


def test__format_processor(format_template: str) -> None:
    # Arrange
    template_container: Mapping[str, object] = {"host": "myInsertedHost", "port": 99999}
    format_processor = FormatProcessor(template_container)

    # Act
    actual = format_processor(format_template)

    # Assert
    assert '"host": "myInsertedHost"' in actual
    assert '"port": 99999' in actual


def test__jinja_processor(jinja_template: str) -> None:
    # Arrange
    template_container: Mapping[str, object] = {"host": "myInsertedHost", "port": 99999}
    jinja_processor = JinjaProcessor(template_container)

    # Act
    actual = jinja_processor(jinja_template)

    # Assert
    assert '"host": "myInsertedHost"' in actual
    assert '"port": 99999' in actual


def test__format_processor__with_missing_key(format_template: str) -> None:
    with pytest.raises(KeyError) as exception:
        # Arrange
        template_container: Mapping[str, object] = {"port": 99999}
        format_processor = FormatProcessor(template_container)

        # Act
        format_processor(format_template)

    # Assert
    assert str(exception) == "<ExceptionInfo KeyError('host') tblen=4>"


def test__jinja_processor__with_missing_key(jinja_template: str) -> None:
    # Arrange
    template_container: Mapping[str, object] = {"port": 99999}
    jinja_processor = JinjaProcessor(template_container)

    # Act
    actual = jinja_processor(jinja_template)

    # Assert
    assert '"host": ""' in actual
    assert '"port": 99999' in actual
