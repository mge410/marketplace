from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
import uuid

from ..helpers.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    uuid: Mapped[str] = mapped_column(
        String(36), unique=True, default=lambda: str(uuid.uuid4())
    )
