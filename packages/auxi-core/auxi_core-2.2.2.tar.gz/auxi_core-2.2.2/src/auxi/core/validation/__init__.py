r"""
Provide data validation tools based on Pydantic.

## Validated Types


### Floating Point Numbers

| Type                   | Validation Rule                  |
| :--------------------- | :------------------------------- |
| `floatFraction`        | 0.0 <= value <= 1.0              |
| `floatNegative`        | value < 0.0                      |
| `floatNegativeOrZero`  | value <= 0.0                     |
| `floatPositive`        | value > 0.0                      |
| `floatPositiveOrZero`  | value >= 0.0                     |
| `listFloatFraction`    | 0.0 <= value[i] <= 1.0 for all i |


### Integer Numbers

| Type                   | Validation Rule |
| :--------------------- | :-------------- |
| `intNegative`          | value < 0       |
| `intNegativeOrZero`    | value <= 0      |
| `intPositive`          | value > 0       |
| `intPositiveOrZero`    | value >= 0      |


### Strings

| Type            | Validation Rule  |
| :-------------- | :--------------- |
| `strNotEmpty`   | len(value) > 0   |
"""

from ._floats import (
    check_fraction,
    check_fraction_list,
    floatFraction,
    floatNegative,
    floatNegativeOrZero,
    floatPositive,
    floatPositiveOrZero,
    listFloatFraction,
)
from ._ints import (
    intNegative,
    intNegativeOrZero,
    intPositive,
    intPositiveOrZero,
)
from ._strings import (
    strNotEmpty,
)


__all__ = [
    "check_fraction",
    "check_fraction_list",
    "floatFraction",
    "floatPositive",
    "floatPositiveOrZero",
    "floatNegative",
    "floatNegativeOrZero",
    "listFloatFraction",
    "intPositive",
    "intPositiveOrZero",
    "intNegative",
    "intNegativeOrZero",
    "strNotEmpty",
]
