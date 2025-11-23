from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import PostModel, UserModel, CategoryModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.repositories.create_post import CreatePost
from src.posts.repositories.implementation.post_builder import (
    CreatePostData,
    PostBuilder,
)
from src.posts.schemes.create_post_schema import CreatePostSchema


class CreatePostImpl(CreatePost):
    def __init__(self, session: AsyncSession, builder: PostBuilder):
        self.session = session
        self.builder = builder

    async def create(self, data: CreatePostSchema, author_id: UUID) -> PostModel:
        author = await self._get_author(author_id)
        await self._ensure_category_exists(data.category_id)
        return await self._make_post(data, author)

    async def _ensure_category_exists(self, category_id: int) -> None:
        query = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        if query.scalar_one_or_none() is None:
            raise CategoryDoesNotExistsException

    async def _get_author(self, author_id: UUID) -> UserModel:
        query = await self.session.execute(
            select(UserModel).where(UserModel.uuid == author_id)
        )
        author = query.scalar_one_or_none()
        if author is None:
            raise UserNotFoundException
        return author

    async def _make_post(self, data: CreatePostSchema, author: UserModel) -> PostModel:
        return await self.builder.build(
            CreatePostData(**data.model_dump(), author_id=author.id)
        )
