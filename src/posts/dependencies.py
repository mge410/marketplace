from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.posts.repositories.implementation.create_category_impl import (
    CreateCategoryImpl,
)
from src.posts.repositories.implementation.create_post_impl import CreatePostImpl
from src.posts.repositories.implementation.delete_post_impl import DeletePostImpl
from src.posts.repositories.implementation.get_list_of_categories_impl import (
    GetListOfCategoriesImpl,
)
from src.posts.repositories.implementation.get_list_of_posts_impl import (
    GetListOfPostsImpl,
)
from src.posts.use_cases.create_category import CreateCategory
from src.posts.use_cases.create_post import CreatePost
from src.posts.use_cases.delete_post import DeletePost
from src.posts.use_cases.get_list_of_categories import GetListOfCategories
from src.posts.use_cases.get_list_of_posts import GetListOfPosts


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


def get_list_of_posts_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> GetListOfPosts:
    repository = GetListOfPostsImpl(session)
    return GetListOfPosts(repository)


def create_posts_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> CreatePost:
    repository = CreatePostImpl(session)
    return CreatePost(repository)


def delete_posts_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> DeletePost:
    repository = DeletePostImpl(session)
    return DeletePost(repository)
