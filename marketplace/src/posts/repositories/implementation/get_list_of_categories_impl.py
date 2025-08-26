from typing import Sequence
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import CategoryModel
from src.posts.repositories.get_list_of_categories import GetListOfCategories

class GetListOfCategoriesImpl(GetListOfCategories):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list_of_categories(self) -> Sequence[CategoryModel]:
        query = select(CategoryModel)
        result = await self.session.execute(query)
        categories = result.scalars().all()

        return categories
