from logging import INFO, LogRecord
from typing import cast

import pytest

from sag_py_logging.console_extra_field_filter import ConsoleExtraFieldFilter
from sag_py_logging.models import ExtraFieldsLogRecord
from tests.test_data.extra_data_test_classes import ClassWithoutDict, NotSerializableClass


@pytest.fixture(name="log_record")
def fixture_log_record() -> LogRecord:
    return LogRecord(name="", level=INFO, pathname="", lineno=0, msg="Hello, world!", args=(), exc_info=None)


def test_without_extra_fields(log_record: LogRecord) -> None:
    # Arrange
    filter_ = ConsoleExtraFieldFilter()

    # Act
    filter_.filter(log_record)

    # Assert
    assert cast(ExtraFieldsLogRecord, log_record).stringified_extra == ""


def test_with_extra_fields(log_record: LogRecord) -> None:
    # Arrange
    filter_ = ConsoleExtraFieldFilter()
    log_record.my_extra_string = "test"
    log_record.my_extra_int = 1
    log_record.my_extra_bool = True
    log_record.my_extra_dict_object = {"keyOne": "valueOne", "keyTwo": 2}
    log_record.my_extra_not_serializable_object = NotSerializableClass("test")
    log_record.my_extra_object_without_dict = ClassWithoutDict(x=123, y=456)

    # Act
    filter_.filter(log_record)

    # Assert
    assert (
        cast(ExtraFieldsLogRecord, log_record).stringified_extra == 'my_extra_string="test", '
        "my_extra_int=1, "
        "my_extra_bool=true, "
        'my_extra_dict_object={"keyOne": "valueOne", "keyTwo": 2}, '
        'my_extra_not_serializable_object={"testtext": "test"}, '
        "my_extra_object_without_dict=ClassWithoutDict(x=123, y=456)"
    )


def test_with_extra_fields_when_called_twice(log_record: LogRecord) -> None:
    # Arrange
    filter_ = ConsoleExtraFieldFilter()
    log_record.my_extra_string = "test"
    log_record.my_extra_int = 1
    log_record.my_extra_bool = True
    log_record.my_extra_dict_object = {"keyOne": "valueOne", "keyTwo": 2}
    log_record.my_extra_not_serializable_object = NotSerializableClass("test")
    log_record.my_extra_object_without_dict = ClassWithoutDict(x=123, y=456)

    # Act
    filter_.filter(log_record)
    filter_.filter(log_record)

    # Assert
    assert (
        cast(ExtraFieldsLogRecord, log_record).stringified_extra == 'my_extra_string="test", '
        "my_extra_int=1, "
        "my_extra_bool=true, "
        'my_extra_dict_object={"keyOne": "valueOne", "keyTwo": 2}, '
        'my_extra_not_serializable_object={"testtext": "test"}, '
        "my_extra_object_without_dict=ClassWithoutDict(x=123, y=456)"
    )
