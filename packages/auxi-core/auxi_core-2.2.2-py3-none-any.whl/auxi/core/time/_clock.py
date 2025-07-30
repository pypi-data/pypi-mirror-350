import datetime as dt
from typing import Any

from dateutil.relativedelta import relativedelta
from pydantic import field_serializer

from ..objects._named_object import NamedObject
from ..validation._ints import intPositive, intPositiveOrZero
from ._time_period import TimePeriod


class Clock(NamedObject):
    """
    A clock that provides functions to manage a ticking clock based on a time period as well as retrieve the current tick's date since the start date.

    :param name: The name.
    :param description: The description.
    :param start_datetime: The start datetime.
    :param timestep_period: The duration of each time period.
    :param timestep_period_count: The number of periods that makes up a timestep.
    """

    # config
    start_datetime: dt.datetime = dt.datetime.min
    timestep_period: TimePeriod = TimePeriod.MONTH
    timestep_period_count: intPositive = 1

    # state
    timestep_index: intPositiveOrZero = 0

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        # config
        self._delta = self._get_period_delta() * self.timestep_period_count

        # state
        self._datetime: dt.datetime = self.start_datetime

    def _init(self) -> None:
        return

    def tick(self) -> None:
        """Increment the clock's timestep index."""
        self.timestep_index += 1
        self._datetime += self._delta

    def reset(self) -> None:
        """Reset the clock's timestep index to '0'."""
        self.timestep_index = 0
        self._datetime = self.start_datetime

    @property
    def datetime(self) -> dt.datetime:
        """The clock's current date and time."""
        return self._datetime

    @property
    def delta(self) -> relativedelta:
        """Timestep duration."""
        return self._delta

    def _get_period_delta(self, index: int = 1) -> relativedelta:
        match self.timestep_period:
            case TimePeriod.MICROSECOND:
                return relativedelta(microseconds=index)
            case TimePeriod.MILLISECOND:
                return relativedelta(microseconds=index)
            case TimePeriod.SECOND:
                return relativedelta(seconds=index)
            case TimePeriod.MINUTE:
                return relativedelta(minutes=index)
            case TimePeriod.HOUR:
                return relativedelta(hours=index)
            case TimePeriod.DAY:
                return relativedelta(days=index)
            case TimePeriod.WEEK:
                return relativedelta(weeks=index)
            case TimePeriod.MONTH:
                return relativedelta(months=index)
            case TimePeriod.YEAR:
                return relativedelta(years=index)

    def get_datetime(self, index: int = 0) -> dt.datetime:
        """
        Get the clock's current datetime, or the specified number of timesteps into the future.

        :index index: Timestamp index.
        :returns: Datetime.
        """
        return self._datetime + self._delta * index

    @field_serializer("timestep_period")
    def serialize_timestep_period(
        self,
        timestep_period: TimePeriod,
    ) -> str | None:
        """Serialize the field."""
        return str(timestep_period)
