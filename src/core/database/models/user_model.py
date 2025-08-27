import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..helpers.base_model import BaseModel

if TYPE_CHECKING:
    from .. import PostModel


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

    posts: Mapped[list["PostModel"]] = relationship(back_populates="author")
