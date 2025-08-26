from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import CategoryModel
from src.posts.repositories.create_category import CreateCategory
from src.posts.schemes.create_category_schema import CreateCategorySchema


class CreateCategoryImpl(CreateCategory):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(
        self, data: CreateCategorySchema
    ) -> CategoryModel | None:
        category = CategoryModel(
            **data.model_dump(),
        )
        self.session.add(category)
        await self.session.commit()

        return category
