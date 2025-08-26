from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..helpers.base_model import BaseModel

if TYPE_CHECKING:
    from .. import PostModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    posts: Mapped[list["PostModel"]] = relationship(back_populates="category")
