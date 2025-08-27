from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    uuid: UUID
    email: EmailStr = Field(description="Уникальный email пользователя")
    phone: str = Field(..., description="Уникальный номер телефона")
    name: str = Field(
        ..., description="Имя пользователя (2-25 символов)", min_length=2, max_length=25
    )
