"""Provide tests."""


def test_import_package() -> None:
    """
    Test importing the sub-package.
    """
    from auxi.core import time

    assert time is not None


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.core.time import (
        Clock,
        TimePeriod,
    )

    assert Clock is not None
    assert TimePeriod is not None
