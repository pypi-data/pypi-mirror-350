"""Provide tests."""

from datetime import datetime

from auxi.core.time import Clock, TimePeriod


def test_constructor(year_clock: Clock) -> None:
    """Test class constructor."""
    assert year_clock.name == "Year Clock"
    assert year_clock.description == "Year clock."
    assert year_clock.start_datetime == datetime(2024, 1, 1)
    assert year_clock.timestep_period == TimePeriod.YEAR
    assert year_clock.timestep_period_count == 1
    assert year_clock.timestep_index == 0


def test_validation(year_clock: Clock) -> None:
    """Test class validation."""
    import pytest

    o_dict = dict(year_clock)
    o_dict["timestep_index"] = -1
    with pytest.raises(ValueError, match="equal to or greater than 0"):
        Clock(**o_dict)

    o_dict = dict(year_clock)
    o_dict["timestep_period_count"] = 0
    with pytest.raises(ValueError, match="greater than 0"):
        Clock(**o_dict)


def test_write(clocks: list[Clock]) -> None:
    """Test the method."""
    import json
    import tempfile
    from pathlib import Path
    from typing import Any
    import yaml

    loaders: dict[str, Any] = {
        ".json": json.loads,
        ".yaml": yaml.safe_load,
    }

    for clock in clocks:
        for suffix, loader in loaders.items():
            f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)

            clock.write(f)
            str_o: str = f.read_text()
            dict_o: dict[str, Any] = loader(str_o)
            new_o: Clock = Clock(**dict_o)

            assert isinstance(new_o, Clock)
            assert str(clock) == str(new_o)
            assert clock.name == new_o.name
            assert clock.description == new_o.description
            assert clock.start_datetime == new_o.start_datetime
            assert clock.timestep_period == new_o.timestep_period
            assert clock.timestep_period_count == new_o.timestep_period_count


def test_read(clocks: list[Clock]) -> None:
    "Test the method." ""
    import tempfile
    from pathlib import Path

    suffixes: list[str] = [".json", ".yaml"]

    for clock in clocks:
        for suffix in suffixes:
            f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)

            clock.write(f)

            new_o: Clock = Clock.read(f)

            assert isinstance(new_o, Clock)
            assert str(clock) == str(new_o)
            assert clock.name == new_o.name
            assert clock.description == new_o.description


def test_tick(hour_clock: Clock) -> None:
    """Test the class method."""
    assert hour_clock.timestep_index == 0
    hour_clock.tick()
    assert hour_clock.timestep_index == 1


def test_reset(hour_clock: Clock) -> None:
    """Test the class method."""
    hour_clock.tick()
    hour_clock.reset()
    assert hour_clock.timestep_index == 0


def test_get_datetime(
    clocks: list[Clock],
) -> None:
    """Test the class method."""
    for clock in clocks:
        assert clock.get_datetime() == datetime(2024, 1, 1)
        assert clock.datetime == datetime(2024, 1, 1)


def test_get_datetime_at(
    clocks: list[Clock],
) -> None:
    """Test the class method."""
    for clock in clocks:
        assert clock.get_datetime(5) == datetime(2024, 1, 1) + 5 * clock.delta
