from typing import List
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime
from .common import BaseModel, PasswordField, PositiveStringField

PhoneNumber.phone_format = "E164"  # 'INTERNATIONAL', 'NATIONAL'


class UserCreateRequestSchema(BaseModel):
    display_name: PositiveStringField
    email: EmailStr
    password: PasswordField
    phone: PhoneNumber

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "display_name": "display name",
                    "email": "email@email.com",
                    "password": "Password123!",
                    "phone": "+381621756244",
                }
            ]
        }
    }


class UserEmailSchema(BaseModel):
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@test.com",
                }
            ]
        }
    }


class UserPhoneSchema(BaseModel):
    phone: PhoneNumber

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phone": "+381621756244",
                }
            ]
        }
    }


class UserResetPasswordSchema(BaseModel):
    code: int
    password: PasswordField

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "123456",
                    "password": "Password123!",
                }
            ]
        }
    }


class UserResponseSchema(BaseModel):
    id: int
    created_at: datetime
    display_name: str
    email: EmailStr
    phone: str
    is_email_verified: bool
    is_phone_verified: bool
    image: str | None = None
    is_superuser: bool


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str

class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordField

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "email@email.com",
                    "password": "Password123!",
                }
            ]
        }
    }


class PaginationUserResponseSchema(BaseModel):
    page: int
    size: int
    total: int
    items: List[UserResponseSchema] | None = []


class UserCodesSchema(BaseModel):
    phone_code: int | None = None
    email_code: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [{"phone_code": 123456, "email_code": 123456}]
        }
    }


class UserRefreshTokenSchema(BaseModel):
    refresh_token: str


class UserResendVerificationResponseSchema(BaseModel):
    email_sent: bool
    sms_sent: bool


class UserResendVerificationRequestSchema(BaseModel):
    user_id: int
