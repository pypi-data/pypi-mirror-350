from ctypes import *
from datetime import datetime, timedelta, timezone

class _Date(Structure):
    _fields_ = [
        ("year", c_short),
        ("month", c_short),
        ("day", c_short),
        ("hour", c_short),
        ("minute", c_short),
        ("second", c_short),
        ("tz_sign", c_short),
        ("tz_hour", c_short),
        ("tz_minute", c_short),
    ]

    # Method to convert _Date structure to Python datetime
    def _to_datetime(self) -> datetime:
        tz_offset = timedelta(hours=self.tz_hour, minutes=self.tz_minute)
        if self.tz_sign == -1:
            tz_offset = -tz_offset

        tz_info = timezone(tz_offset)

        # Create and return the datetime object
        dt = datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            tzinfo=tz_info
        )
        return dt

    # Class method to create a _Date structure from a datetime object
    @classmethod
    def _from_datetime(cls, dt: datetime):
        if datetime is None:
            return None
        if dt.tzinfo is not None:
            total_offset = dt.utcoffset().total_seconds() // 60  # Total minutes
            tz_sign = 1 if total_offset >= 0 else -1
            tz_hour = abs(total_offset) // 60
            tz_minute = abs(total_offset) % 60
        else:
            tz_sign = 0  # No timezone
            tz_hour = 0
            tz_minute = 0

        # Create and return a _Date structure
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            tz_sign=tz_sign,
            tz_hour=tz_hour,
            tz_minute=tz_minute
        )