"""Provide tests."""


def test_import_package() -> None:
    """
    Test importing the sub-package.
    """
    from auxi.core import reporting

    assert reporting is not None


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.core.reporting import (
        Report,
        ReportFormat,
    )

    assert Report is not None
    assert ReportFormat is not None
