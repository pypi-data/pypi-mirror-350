from enum import IntEnum


class TimePeriod(IntEnum):
    """A period of time."""

    MICROSECOND = 0
    MILLISECOND = 1
    SECOND = 2
    MINUTE = 3
    HOUR = 4
    DAY = 5
    WEEK = 6
    MONTH = 7
    YEAR = 8
