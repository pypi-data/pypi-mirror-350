"""Implementation of the primitive data arranger.

Provides an interface and default implementation for transforming raw primitive input values
into typed representations, including support for common types like strings, numbers, and dates."""

import re
from datetime import datetime
from abc import ABC
from typing import Optional, Any


class IArranger(ABC):
    """Arranger interface in charge of processing primitive data by type.

    Example
    -------
    arrangeData("420.4", dtype="number", defaultValue=100) -> 420.4
    arrangeData("", dtype="number", defaultValue=100) -> 100
    arrangeData("", dtype="number") -> None
    """

    datetime_processors = {
        "iso": lambda x: x.isoformat(),
        "year": lambda x: x.year,
        "day": lambda x: x.day,
        "month": lambda x: x.month,
        "weekday": lambda x: x.weekday(),
        "hour": lambda x: x.hour,
        "minute": lambda x: x.minute,
        "timestamp": lambda x: x.timestamp(),
        "time": lambda x: x.time(),
        "date": lambda x: x.date(),
        "fold": lambda x: x.fold,
    }

    def __init__(self):
        """Initializes the arranger with internal type processors."""
        self.__processors = {
            # datetime
            "datetime": self.__process_datetime,
            "date": self.__process_datetime,
            # string
            "string": self.__process_string,
            "str": self.__process_string,
            # numbers
            "number": self.__process_number,
            "float": self.__process_number,
            "decimal": self.__process_number,

            "integer": self.__process_integer,
            "int": self.__process_integer,

            # enum
            "enum": self.__process_enum,

            # no type
            "-": self.__process_not_type
        }

    @staticmethod
    def process_datetime_when_is_string(value, date_format="iso") -> Optional[datetime]:
        """Converts a string to a datetime object using the given format.

        Parameters
        ----------
        value : str
            The string representing a date or timestamp.
        date_format : str, optional
            The format to interpret the string, by default "iso".

        Returns
        -------
        Optional[datetime]
            A datetime object if successfully parsed, else None.
        """
        res = None
        if date_format == "iso":
            try:
                res = datetime.fromisoformat(value)
            except ValueError:
                pass
        elif date_format == "timestamp" and value.replace(".", "", 1).isdigit():
            res = datetime.fromtimestamp(float(value))
        else:
            try:
                res = datetime.strptime(value, date_format)
            except ValueError:
                pass
        return res

    @staticmethod
    def __process_datetime(value, date_format="iso", default_value=None,
                           transform=None, *_, **__) -> Optional[Any]:
        """Processes a datetime input, applying formatting or transformations if needed.

        Parameters
        ----------
        value : Any
            The value to convert to datetime.
        date_format : str, optional
            Format to interpret strings, by default "iso".
        default_value : Any, optional
            Value to return if parsing fails or value is None.
        transform : str, optional
            A datetime attribute to extract (e.g., "year", "timestamp").

        Returns
        -------
        Optional[Any]
            A datetime, transformed value, or timestamp; None if invalid.
        """
        res = None
        if isinstance(value, datetime):
            res = value
        elif isinstance(value, (float, int)):
            res = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            res = IArranger.process_datetime_when_is_string(value, date_format)

        if res is None and default_value == "now":
            res = datetime.now()

        if transform is not None and isinstance(res, datetime):
            res = IArranger.datetime_processors.get(transform, lambda x: x)(res)
        elif isinstance(res, datetime):
            res = res.timestamp()
        return res

    @staticmethod
    def __process_enum(value, enum, *_, **__) -> Optional[Any]:
        """Validates if a value is a member of the provided enum.

        Parameters
        ----------
        value : Any
            Value to check.
        enum : iterable
            Collection of valid enum values.

        Returns
        -------
        Optional[Any]
            The original value if valid, otherwise None.
        """
        if value in enum:
            return value
        return None

    @staticmethod
    def __process_string(value, default_value: Optional[str] = None, *_, **__) -> str:
        """Casts the value to a string.

        Parameters
        ----------
        value : Any
            Value to convert.

        Returns
        -------
        str
            String representation of the input.
        """
        return str(value) if value is not None else default_value

    @staticmethod
    def __process_integer(value, *_, **__) -> Optional[int]:
        """Converts the input to an integer if possible.

        Parameters
        ----------
        value : Any
            Value to convert.

        Returns
        -------
        Optional[int]
            Integer value, or None if invalid.
        """
        if isinstance(value, int):
            return value
        if (isinstance(value, str) and re.fullmatch(r"\d+\.?0*", value)) or \
                isinstance(value, bool):
            return int(float(value))
        return None

    @staticmethod
    def __process_number(value, *_, **__) -> Optional[float]:
        """Converts the input to a float if possible.

        Parameters
        ----------
        value : Any
            Value to convert.

        Returns
        -------
        Optional[float]
            Float or integer value, or None if invalid.
        """
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if value.isdigit():
                return int(value)
            if value.replace(".", "", 1).isdigit():
                return float(value)
        return None

    @staticmethod
    def __process_not_type(value, *_, **__) -> Any:
        """
        Passes the value through unmodified.

        Parameters
        ----------
        value : Any
            Value to return.

        Returns
        -------
        Any
            Same as input value.
        """
        return value

    def arrange_value(self, value, dtype: str= "-", default_value=None, *args, **kwargs) -> Any:
        """Processes and transforms a primitive value based on type.

        Parameters
        ----------
        value : Any
            The raw input value.
        dtype : str, optional
            The declared type of the value (e.g., "string", "number").
        default_value : Any, optional
            Value to use if transformation returns None.

        Returns
        -------
        Any
            Transformed value or default.
        """
        if dtype in self.__processors:
            _process = self.__processors[dtype]
            res = _process(value, default_value=default_value, *args, **kwargs)
            if res is not None:
                return res
        return default_value
