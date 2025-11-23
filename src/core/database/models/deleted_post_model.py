from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..helpers.base_model import BaseModel

if TYPE_CHECKING:
    from .. import CategoryModel
    from .. import UserModel


class DeletedPostModel(BaseModel):
    __tablename__ = "deleted_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["CategoryModel"] = relationship(back_populates="deleted_posts")

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["UserModel"] = relationship(back_populates="deleted_posts")

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
