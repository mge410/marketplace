from typing import List

from src.posts.repositories.get_list_of_categories import (
    GetListOfCategories as GetListOfCategoriesRepository,
)
from src.posts.schemes.category_schema import CategorySchema


class GetListOfCategories:
    def __init__(self, repository: GetListOfCategoriesRepository):
        self.repository = repository

    async def get_list_of_category(self) -> List[CategorySchema]:
        categories = await self.repository.get_list_of_categories()
        return [
            CategorySchema(id=category.id, title=category.title)
            for category in categories
        ]
