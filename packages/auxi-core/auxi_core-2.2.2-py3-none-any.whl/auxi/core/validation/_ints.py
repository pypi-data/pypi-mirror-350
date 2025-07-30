from typing import Annotated
from pydantic import AfterValidator, ValidationInfo


def int_p(
    v: int,
    info: ValidationInfo,
) -> int:
    if v <= 0:
        raise ValueError(f"{info.field_name} must be greater than 0.")

    return v


intPositive = Annotated[
    int,
    AfterValidator(int_p),
]


def int_pz(
    v: int,
    info: ValidationInfo,
) -> int:
    if v < 0:
        raise ValueError(f"{info.field_name} must be equal to or greater than 0.")

    return v


intPositiveOrZero = Annotated[
    int,
    AfterValidator(int_pz),
]


def int_n(
    v: int,
    info: ValidationInfo,
) -> int:
    if v >= 0:
        raise ValueError(f"{info.field_name} must be less than 0.")

    return v


intNegative = Annotated[
    int,
    AfterValidator(int_n),
]


def int_nz(
    v: int,
    info: ValidationInfo,
) -> int:
    if v > 0:
        raise ValueError(f"{info.field_name} must be equal to or less than 0.")

    return v


intNegativeOrZero = Annotated[
    int,
    AfterValidator(int_nz),
]
