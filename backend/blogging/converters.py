"""Custom path parameter converters are here."""
from datetime import datetime, date
from typing import Union, Literal

from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):
    """Convert between date strings to date objects.

    Only understood format is dd-mm-yyyy, where for days and months
    the second digit is optional.
    """

    regex = r"(\d\d?-\d\d?-\d{4})|(any)"

    def __init__(self, url_map, date: Union[str, Literal["any"]] = "any"):
        super().__init__(url_map)
        self._date = date

    def to_python(self, value: str) -> Union[date, bool]:
        """Convert to Python."""

        as_list = [int(x) for x in value.split("-")]
        if as_list[0] == "any":
            return True
        if not (0 < as_list[0] <= 31 and
                0 < as_list[1] <= 12):
            raise ValidationError("Given date or month is invalid.")

        return date(day=as_list[0], month=as_list[1], year=as_list[2])

    def to_url(self, d: Union[date, bool]) -> str:
        """Convert to url."""

        if d is True:
            return "any"
        return f"{d.day}-{d.month}-{d.year}"
