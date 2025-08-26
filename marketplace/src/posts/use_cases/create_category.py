from src.posts.repositories.create_category import (
    CreateCategory as CreateCategoryRepository,
)
from src.posts.schemes.create_category_schema import CreateCategorySchema


class CreateCategory:
    def __init__(self, repository: CreateCategoryRepository):
        self.repository = repository

    async def create_category(self, data: CreateCategorySchema) -> None:
       await self.repository.create_category(data)
