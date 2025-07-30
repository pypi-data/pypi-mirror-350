import csv
from io import StringIO
from pathlib import Path
from typing import Any

from pydantic import field_serializer
from tabulate import tabulate

from auxi.core.objects import Object

from ._report_format import ReportFormat


class Report(Object):
    """
    Abstract base class for all auxi reports.

    :param data_source: An object with data to be used in the report.
    :param output_path: The path where the report should be saved.
    """

    data_source: Any
    output_path: Path | None = None

    @field_serializer("output_path")
    def serialize_output_path(
        self,
        output_path: Path | None,
    ) -> str | None:
        """Serialize the field."""
        if output_path is None:
            result = output_path
        else:
            result = str(output_path)

        return result

    def _generate_table_(self) -> list[list[Any]]:
        return self.data_source

    def _render_matplotlib_(self, png: bool = False) -> None:
        pass

    def render(self, format: ReportFormat = ReportFormat.PRINT) -> str | None:
        """
        Render the report in the specified format.

        :param format: The format. The default format is to print the report to the console.
        :returns: If the format was set to 'string' then a string representation of the report is returned.
        """
        table = self._generate_table_()

        match format:
            case ReportFormat.PRINT:
                print(tabulate(table, headers="firstrow", tablefmt="simple"))
            case ReportFormat.LATEX:
                self._render_latex_(table)
            case ReportFormat.TXT:
                self._render_txt_(table)
            case ReportFormat.CSV:
                self._render_csv_(table)
            case ReportFormat.STRING:
                return str(tabulate(table, headers="firstrow", tablefmt="simple"))
            case ReportFormat.MATPLOTLIB:
                self._render_matplotlib_()
            case ReportFormat.PNG:
                if self.output_path is None:
                    self._render_matplotlib_()
                else:
                    self._render_matplotlib_(True)

    def _render_latex_(self, table: list[list[Any]]) -> None:
        if self.output_path is not None:
            with open(self.output_path.with_suffix(".tex"), "w") as f:
                f.write(tabulate(table, headers="firstrow", tablefmt="latex"))
        else:
            print(tabulate(table, headers="firstrow", tablefmt="latex"))

    def _render_txt_(self, table: list[list[Any]]) -> None:
        if self.output_path is not None:
            with open(self.output_path.with_suffix(".txt"), "w") as f:
                f.write(tabulate(table, headers="firstrow", tablefmt="simple"))
        else:
            print(tabulate(table, headers="firstrow", tablefmt="simple"))

    def _render_csv_(self, table: list[list[Any]]) -> None:
        if self.output_path is not None:
            with open(self.output_path.with_suffix(".csv"), "w") as f:
                csv.writer(f, lineterminator="\n").writerows(table)
        else:
            with StringIO() as f:
                csv.writer(f, lineterminator="\n").writerows(table)
                print(f.getvalue())
