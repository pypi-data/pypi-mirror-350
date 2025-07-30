from enum import IntEnum


class ReportFormat(IntEnum):
    """Report output format."""

    PRINT = 1
    LATEX = 2
    TXT = 3
    CSV = 4
    STRING = 5
    MATPLOTLIB = 6
    PNG = 7
