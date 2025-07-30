from typing import Annotated
from pydantic import AfterValidator, ValidationInfo


# region re-usable checks


def check_fraction(
    v: float,
    field_name: str | None,
) -> float:
    fn = "" if field_name is None else f"{field_name} "

    if v < 0.0 or v > 1.0:
        raise ValueError(f"{fn}value must be between zero and one, inclusive.")

    return v


def check_fraction_list(
    v: list[float],
    field_name: str | None,
) -> list[float]:
    fn = "" if field_name is None else f"{field_name} "

    result = [check_fraction(vv, fn) for vv in v]

    if 1.0 - abs(sum(result)) > 1.0e-12:
        raise ValueError(f"{fn}'s elements must add up to 1.0, within machine precision.")

    return result


# endregion re-usable checks


def float_p(
    v: float,
    info: ValidationInfo,
) -> float:
    if v <= 0.0:
        raise ValueError(f"{info.field_name} must be greater than 0.0.")

    return v


floatPositive = Annotated[
    float,
    AfterValidator(float_p),
]


def float_pz(
    v: float,
    info: ValidationInfo,
) -> float:
    if v < 0.0:
        raise ValueError(f"{info.field_name} must be equal to or greater than 0.0.")

    return v


floatPositiveOrZero = Annotated[
    float,
    AfterValidator(float_pz),
]


def float_n(
    v: float,
    info: ValidationInfo,
) -> float:
    if v >= 0.0:
        raise ValueError(f"{info.field_name} must be less than 0.0.")

    return v


floatNegative = Annotated[
    float,
    AfterValidator(float_n),
]


def float_nz(
    v: float,
    info: ValidationInfo,
) -> float:
    if v > 0.0:
        raise ValueError(f"{info.field_name} must be equal to or less than 0.0.")

    return v


floatNegativeOrZero = Annotated[
    float,
    AfterValidator(float_nz),
]


def float_fraction(
    v: float,
    info: ValidationInfo,
) -> float:
    return check_fraction(v, info.field_name)


floatFraction = Annotated[
    float,
    AfterValidator(float_fraction),
]


def float_fraction_list(
    v: list[float],
    info: ValidationInfo,
) -> list[float]:
    return check_fraction_list(v, info.field_name)


listFloatFraction = Annotated[
    list[floatFraction],
    AfterValidator(float_fraction),
]
