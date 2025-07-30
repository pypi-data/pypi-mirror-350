"""Provide test fixtures."""

from typing import Any

import pytest

from auxi.core.reporting import Report


class ConcreteReport(Report):
    """Concrete class for testing."""

    def _init(self) -> None:
        return


@pytest.fixture
def data_source() -> list[list[Any]]:
    """Provide data source for tests."""
    return [["cola", "colb"], [1, 2]]


@pytest.fixture
def report(data_source: list[list[Any]]) -> ConcreteReport:
    """Provide report for tests."""
    result = ConcreteReport(
        data_source=data_source,
    )
    result.init()

    return result


@pytest.fixture
def report_with_path(data_source: list[list[Any]]) -> ConcreteReport:
    """Provide report with output path for tests."""
    from pathlib import Path

    result = ConcreteReport(
        data_source=data_source,
        output_path=Path("./test"),
    )
    result.init()

    return result


@pytest.fixture
def reports(
    report: ConcreteReport,
    report_with_path: ConcreteReport,
) -> list[ConcreteReport]:
    """Provide a list of reports for tests."""
    return [report, report_with_path]
