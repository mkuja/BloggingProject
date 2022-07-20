import re
from datetime import datetime

from marshmallow import fields


class MyDateTimeField(fields.Field):
    """Field that serializes datetime to a string and a string to a datetime object.
    """

    regexp = re.compile(r"(\d\d?).(\d\d?).(\d{4}), (\d\d?):(\d\d?)")

    # TODO: Implement and test.
    def _deserialize(self, value: datetime, attr, obj, **kwargs):
        m = self.regexp.match(value)
        return datetime(day=int(m.group(1)),
                        month=int(m.group(2)),
                        year=int(m.group(3)),
                        hour=int(m.group(4)),
                        minute=int(m.group(5)))

    def _serialize(self, value: datetime, attr, data, **kwargs):
        if isinstance(value, str):
            return value
        return f"{value.day}.{value.month}.{value.year}, {value.hour}:{value.minute}"

