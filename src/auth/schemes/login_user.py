from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.core.config import settings


class LoginUserSchema(BaseModel):
    email: EmailStr = Field(description="Уникальный email пользователя")
    password: str = Field(
        description="Пароль (6-16 символа)", min_length=6, max_length=16
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
            }
        }
    )


class TokenPayload(BaseModel):
    sub: str
    uuid: str
    email: str
    name: str
    phone: str
    exp: int = settings.auth_jwt.access_token_expire_minutes


class TokenInfo(BaseModel):
    token: str
    token_type: str
    max_age: int
