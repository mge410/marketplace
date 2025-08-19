import re

from pydantic import constr, Field, field_validator

from src.auth.schemes.login_user import LoginUserSchema


class RegisterUserSchema(LoginUserSchema):
    phone: str = Field(..., description="Уникальный номер телефона")
    name: constr(min_length=2, max_length=25) = Field(..., description="Имя пользователя (2-25 символов)")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        phone_regex = r"^(\+7|8)\d{10}$"
        if not re.match(phone_regex, value):
            raise ValueError("Номер телефона должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "phone": "+79123456789",
                "name": "Иван Петров"
            }
        }
