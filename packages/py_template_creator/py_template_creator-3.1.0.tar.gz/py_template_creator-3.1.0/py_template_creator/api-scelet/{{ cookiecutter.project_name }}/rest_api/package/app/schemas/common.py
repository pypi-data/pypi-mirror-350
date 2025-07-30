from typing import Generic, TypeVar, List, Annotated
from pydantic import (
    BaseModel as PydanticBaseModel,
    ConfigDict,
    AfterValidator,
    Field,
)
from package.app.utilities.enum import JobStatusEnum
import datetime as dt
import logging
from package.app import settings

logger = logging.getLogger(__name__)
DATE_TIME_FORMAT = settings.DATE_TIME_FORMAT
L_DATE_TIME_FORMAT = "{:" + DATE_TIME_FORMAT + "}"


def validate_password(v: str) -> str:
    special_chars = {
        "$",
        "@",
        "#",
        "%",
        "!",
        "?",
        ".",
        ",",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "{",
        "}",
        "[",
        "]",
        "<",
        ">",
    }
    if not isinstance(v, str):
        raise TypeError("string required")
    if len(v) < 8:
        raise ValueError("Password must be at least eight characters long")
    if not any(char.isdigit() for char in v):
        raise ValueError("Password must contain at least one number")
    if not any(char.isupper() for char in v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char in special_chars for char in v):
        raise ValueError("Password must include a special character")
    return v


PasswordField = Annotated[str, AfterValidator(validate_password)]
PositiveField = Annotated[float, Field(gt=0)]
PositiveStringField = Annotated[str, Field(min_length=1)]
T = TypeVar("T")  # Generic Type

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
        json_encoders={
            dt.datetime: lambda d: L_DATE_TIME_FORMAT.format(d)
            # float: lambda f: "{:.2f}".format(f)
            # DONT USE THIS CAUSE: prices in crypto and google location coordinates
        },
    )


class BaseResponseSchema(BaseModel):
    message: str
    errors: dict | None = None
    special_code: int | None = None


class JobResponseSchema(BaseModel):
    job_key: str
    status: JobStatusEnum
    data: dict | None = None


class ValidationErrorResponseSchema(BaseModel):
    message: str | None = "Validation error"
    errors: dict


class CodeSchema(BaseModel):
    code: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 123456,
                }
            ]
        }
    }

class Page(BaseModel, Generic[T]):
    page: int
    size: int
    total: int
    items: List[T] | None = []