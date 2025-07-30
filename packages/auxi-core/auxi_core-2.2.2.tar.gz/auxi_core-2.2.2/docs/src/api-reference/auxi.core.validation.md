# package `auxi.core.validation`

Provide data validation tools.

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
