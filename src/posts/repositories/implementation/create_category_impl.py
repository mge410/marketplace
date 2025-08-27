from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import CategoryModel
from src.posts.exceptions.category_already_exists_exception import (
    CategoryAlreadyExistsException,
)
from src.posts.repositories.create_category import CreateCategory
from src.posts.schemes.create_category_schema import CreateCategorySchema


class CreateCategoryImpl(CreateCategory):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, data: CreateCategorySchema) -> CategoryModel | None:
        await self._check_unique_category(data.title)

        category = CategoryModel(
            **data.model_dump(),
        )
        self.session.add(category)
        await self.session.commit()

        return category

    async def _check_unique_category(self, title: str) -> None:
        existing_category = await self.session.execute(
            select(CategoryModel).where(CategoryModel.title == title)
        )
        if existing_category.scalar_one_or_none():
            raise CategoryAlreadyExistsException
