from abc import ABC, abstractmethod

from src.core.database import CategoryModel
from src.posts.schemes.create_category_schema import CreateCategorySchema


class CreateCategory(ABC):
    @abstractmethod
    async def create_category(self, data: CreateCategorySchema) -> CategoryModel | None:
        pass
