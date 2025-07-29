from datetime import datetime

import pytest

from bisslog.utils.mapping import IArranger


@pytest.fixture
def arranger():
    return IArranger()


@pytest.mark.parametrize("value, expected", [
    ("123.45", 123.45),
    ("100", 100),
    ("abc", None),
    (123, 123),
    (None, None)
])
def test_process_number(arranger, value, expected):
    assert arranger._IArranger__process_number(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("123", 123),
    ("42", 42),
    ("3.14", None),
    ("3.00", 3),
    ("3.", 3),
    ("3.0", 3),
    ("abc", None),
    (True, 1),
    (False, 0),
    (10, 10),
    (None, None)
])
def test_process_integer(arranger, value, expected):
    assert arranger._IArranger__process_integer(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("hello", "hello"),
    (123, "123"),
    (None, None),
    (True, "True"),
])
def test_process_string(arranger, value, expected):
    assert arranger._IArranger__process_string(value) == expected


@pytest.mark.parametrize("value, date_format, expected", [
    ("2023-03-25T14:30:00", "iso", datetime(2023, 3, 25, 14, 30).timestamp()),
    (1679788200, "timestamp", 1679788200),  # Epoch time
    ("1679788200", "timestamp", 1679788200),
    ("03/25/2023", "%m/%d/%Y", datetime(2023, 3, 25).timestamp()),
    ("invalid-date", "iso", None),
    (None, "iso", None),
])
def test_process_datetime(arranger, value, date_format, expected):
    assert arranger._IArranger__process_datetime(value, date_format) == expected


@pytest.mark.parametrize("value, transform, expected", [
    (datetime(2023, 3, 25, 14, 30), "iso", "2023-03-25T14:30:00"),
    (datetime(2023, 3, 25, 14, 30), "year", 2023),
    (datetime(2023, 3, 25, 14, 30), "month", 3),
    (datetime(2023, 3, 25, 14, 30), "day", 25),
    (datetime(2023, 3, 25, 14, 30), "hour", 14),
    (datetime(2023, 3, 25, 14, 30), "minute", 30),
    (datetime(2023, 3, 25, 14, 30), "timestamp", datetime(2023, 3, 25, 14, 30).timestamp()),
    (datetime(2023, 3, 25, 14, 30), "weekday", 5),  # 5 -> Saturday
    (None, "iso", None),
])
def test_process_datetime_transform(arranger, value, transform, expected):
    assert arranger._IArranger__process_datetime(value, transform=transform) == expected


@pytest.mark.parametrize("value, enum, expected", [
    ("apple", ["apple", "banana", "cherry"], "apple"),
    ("orange", ["apple", "banana", "cherry"], None),
    (None, ["apple", "banana"], None)
])
def test_process_enum(arranger, value, enum, expected):
    assert arranger._IArranger__process_enum(value, enum) == expected


@pytest.mark.parametrize("value, expected", [
    ("some_value", "some_value"),
    (123, 123),
    (None, None)
])
def test_process_not_type(arranger, value, expected):
    assert arranger._IArranger__process_not_type(value) == expected


@pytest.mark.parametrize("value, dtype, default_value, expected", [
    ("123", "integer", None, 123),
    ("42.5", "number", None, 42.5),
    ("text", "string", None, "text"),
    (None, "number", 100, 100),
    ("invalid", "number", 50, 50),
    (None, "string", "default_str", "default_str"),
    (None, "-", "fallback", "fallback"),
])
def test_arrange_value(arranger, value, dtype, default_value, expected):
    assert arranger.arrange_value(value, dtype, default_value) == expected


def test_arrange_dt_value_with_now_default():
    arranger = IArranger()
    format_dt = "%Y-%m-%d"
    result = arranger.arrange_value("None", dtype="datetime", date_format=format_dt)
    assert result is None
    result = arranger.arrange_value("2025-11-29", dtype="datetime", date_format=format_dt)
    assert isinstance(result, float)


def test_arrange_value_datetime_now():
    arranger = IArranger()
    result = arranger.arrange_value(None, dtype="datetime", default_value="now")
    assert isinstance(result, float)
    result = arranger.arrange_value("None", dtype="datetime", default_value="now")
    assert isinstance(result, float)


def test_arrange_value_direct_pass_through():
    arranger = IArranger()
    assert arranger.arrange_value("unchanged", dtype="-") == "unchanged"
