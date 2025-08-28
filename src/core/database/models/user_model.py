from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..helpers.base_model import BaseModel

if TYPE_CHECKING:
    from .. import PostModel
    from . import DeletedPostModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False)

    posts: Mapped[list["PostModel"]] = relationship(back_populates="author")
    deleted_posts: Mapped[list["DeletedPostModel"]] = relationship(
        back_populates="author"
    )
