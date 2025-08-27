from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import PostModel, UserModel, CategoryModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.repositories.create_post import CreatePost
from src.posts.schemes.create_post_schema import CreatePostSchema


class CreatePostImpl(CreatePost):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CreatePostSchema, author_id: UUID) -> PostModel:
        await self._check_that_category_exist(data.category_id)
        author = await self._check_that_user_exists(author_id)

        post = PostModel(
            title=data.title,
            content=data.content,
            image_url=data.image_url,
            category_id=data.category_id,
            author_id=author.id,
        )

        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def _check_that_category_exist(self, category_id: int) -> None:
        category_result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        category = category_result.scalar_one_or_none()
        if not category:
            raise CategoryDoesNotExistsException

    async def _check_that_user_exists(self, author_id: UUID) -> UserModel:
        user_result = await self.session.execute(
            select(UserModel).where(UserModel.uuid == author_id)
        )
        author = user_result.scalar_one_or_none()
        if not author:
            raise UserNotFoundException
        return author
