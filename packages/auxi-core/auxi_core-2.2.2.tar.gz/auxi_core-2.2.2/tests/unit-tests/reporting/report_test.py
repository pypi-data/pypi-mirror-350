"""Provide tests."""

from .conftest import ConcreteReport


def test_constructor(
    report: ConcreteReport,
    report_with_path: ConcreteReport,
) -> None:
    """Test class constructor."""
    assert report is not None
    assert len(report.data_source) == 2
    assert report.output_path is None

    assert report_with_path is not None
    assert len(report_with_path.data_source) == 2
    assert report_with_path.output_path is not None


def test_write(reports: list[ConcreteReport]) -> None:
    """Test the method."""
    import json
    import pytest
    import tempfile
    from pathlib import Path
    from typing import Any
    import yaml

    loaders: dict[str, Any] = {".json": json.loads, ".yaml": yaml.safe_load, ".txt": None}

    for report in reports:
        for suffix, loader in loaders.items():
            f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)

            if suffix == ".txt":
                with pytest.raises(ValueError):
                    report.write(f)
            else:
                report.write(f)
                str_o: str = f.read_text()
                dict_o: dict[str, Any] = loader(str_o)
                new_o: ConcreteReport = ConcreteReport(**dict_o)

                assert isinstance(new_o, ConcreteReport)
                assert str(report) == str(new_o)
                assert report.data_source == new_o.data_source
                assert report.output_path == new_o.output_path


def test_read(reports: list[ConcreteReport]) -> None:
    "Test the method." ""
    import pytest
    import tempfile
    from pathlib import Path

    suffixes: list[str] = [".json", ".yaml", ".txt"]

    for report in reports:
        for suffix in suffixes:
            f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)

            if suffix == ".txt":
                f.touch()
                with pytest.raises(ValueError):
                    new_o: ConcreteReport = ConcreteReport.read(f)
            else:
                report.write(f)

                new_o: ConcreteReport = ConcreteReport.read(f)

                assert isinstance(new_o, ConcreteReport)
                assert str(report) == str(new_o)
                assert report.data_source == new_o.data_source
                assert report.output_path == new_o.output_path


def test_render(report: ConcreteReport) -> None:
    """Test class method."""
    from auxi.core.reporting import ReportFormat

    report.render(format=ReportFormat.PRINT)
    report.render(format=ReportFormat.LATEX)
    report.render(format=ReportFormat.TXT)
    report.render(format=ReportFormat.CSV)

    string = report.render(format=ReportFormat.STRING)
    assert string is not None
    assert len(string) > 0

    report.render(format=ReportFormat.MATPLOTLIB)
    report.render(format=ReportFormat.PNG)


def test_render_with_file(report_with_path: ConcreteReport) -> None:
    """Test class method."""
    from auxi.core.reporting import ReportFormat

    file_name = report_with_path.output_path
    assert file_name is not None

    report_with_path.render(format=ReportFormat.PRINT)

    report_with_path.render(format=ReportFormat.LATEX)
    assert file_name.with_suffix(".tex").exists()
    file_name.with_suffix(".tex").unlink()

    report_with_path.render(format=ReportFormat.TXT)
    assert file_name.with_suffix(".txt").exists()
    file_name.with_suffix(".txt").unlink()

    report_with_path.render(format=ReportFormat.CSV)
    assert file_name.with_suffix(".csv").exists()
    file_name.with_suffix(".csv").unlink()

    string = report_with_path.render(format=ReportFormat.STRING)
    assert string is not None
    assert len(string) > 0

    report_with_path.render(format=ReportFormat.MATPLOTLIB)

    report_with_path.render(format=ReportFormat.PNG)
