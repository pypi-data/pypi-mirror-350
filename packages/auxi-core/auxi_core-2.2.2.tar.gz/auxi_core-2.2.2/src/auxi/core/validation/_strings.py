from typing import Annotated
from pydantic import AfterValidator, ValidationInfo


def str_not_empty(
    v: str,
    info: ValidationInfo,
) -> str:
    result = v.strip()

    if len(result) == 0.0:
        raise ValueError(f"{info.field_name} string length must be greater than 0.")

    return v


strNotEmpty = Annotated[
    str,
    AfterValidator(str_not_empty),
]
