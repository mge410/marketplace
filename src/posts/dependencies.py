from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.posts.repositories.implementation.create_category_impl import (
    CreateCategoryImpl,
)
from src.posts.repositories.implementation.get_list_of_categories_impl import (
    GetListOfCategoriesImpl,
)
from src.posts.use_cases.create_category import CreateCategory
from src.posts.use_cases.get_list_of_categories import GetListOfCategories


def get_list_of_categories_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> GetListOfCategories:
    repository = GetListOfCategoriesImpl(session)
    return GetListOfCategories(repository)


def create_category_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> CreateCategory:
    repository = CreateCategoryImpl(session)
    return CreateCategory(repository)
