from src.posts.repositories.create_category import (
    CreateCategory as CreateCategoryRepository,
)
from src.posts.schemes.create_category_schema import CreateCategorySchema


class CreateCategory:
    def __init__(self, repository: CreateCategoryRepository):
        self.repository = repository

    def create_category(self, email: CreateCategorySchema) -> None:
        pass
