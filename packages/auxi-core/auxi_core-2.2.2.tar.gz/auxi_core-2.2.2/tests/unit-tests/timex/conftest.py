"""Provide test fixtures."""

import pytest

from auxi.core.time import Clock


@pytest.fixture
def microsecond_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Microsecond Clock",
        description="Microsecond clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.MICROSECOND,
        timestep_period_count=1,
    )


@pytest.fixture
def millisecond_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Millisecond Clock",
        description="Millisecond clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.MILLISECOND,
        timestep_period_count=1,
    )


@pytest.fixture
def second_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Second Clock",
        description="Second clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.SECOND,
        timestep_period_count=1,
    )


@pytest.fixture
def minute_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Minute Clock",
        description="Minute clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.MINUTE,
        timestep_period_count=1,
    )


@pytest.fixture
def hour_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Hour Clock",
        description="Hour clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.HOUR,
        timestep_period_count=1,
    )


@pytest.fixture
def day_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Day Clock",
        description="Day clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.DAY,
        timestep_period_count=1,
    )


@pytest.fixture
def week_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Week Clock",
        description="Week clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.WEEK,
        timestep_period_count=1,
    )


@pytest.fixture
def month_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Month Clock",
        description="Month clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.MONTH,
        timestep_period_count=1,
    )


@pytest.fixture
def year_clock() -> Clock:
    """Provide an object for testing."""
    from datetime import datetime
    from auxi.core.time import TimePeriod

    return Clock(
        name="Year Clock",
        description="Year clock.",
        start_datetime=datetime(2024, 1, 1),
        timestep_period=TimePeriod.YEAR,
        timestep_period_count=1,
    )


@pytest.fixture
def clocks(
    microsecond_clock: Clock,
    millisecond_clock: Clock,
    second_clock: Clock,
    minute_clock: Clock,
    hour_clock: Clock,
    day_clock: Clock,
    week_clock: Clock,
    month_clock: Clock,
    year_clock: Clock,
) -> list[Clock]:
    """Provide objects for testing."""
    return [
        microsecond_clock,
        millisecond_clock,
        second_clock,
        minute_clock,
        hour_clock,
        day_clock,
        week_clock,
        month_clock,
        year_clock,
    ]
