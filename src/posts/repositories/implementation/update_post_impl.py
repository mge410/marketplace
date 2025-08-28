from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import PostModel, CategoryModel
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.repositories.implementation.mixins.post_access_mixin import (
    PostAccessMixin,
)
from src.posts.repositories.update_post import UpdatePost
from src.posts.schemes.update_post_schema import UpdatePostSchema


class UpdatePostImpl(UpdatePost, PostAccessMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session

    async def update(
        self, post_id: int, data: UpdatePostSchema, author_id: UUID
    ) -> PostModel | None:
        post = await self._find_post_by_id(post_id)
        await self._check_author_access(post, author_id)
        await self._validate_category_exists(data.category_id)

        post.title = data.title
        post.content = data.content
        post.image_url = data.image_url
        post.category_id = data.category_id

        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def _validate_category_exists(self, category_id: int) -> None:
        category_query = select(CategoryModel).where(CategoryModel.id == category_id)
        category_result = await self.session.execute(category_query)

        try:
            category_result.scalar_one()
        except NoResultFound:
            raise CategoryDoesNotExistsException(
                f"Category with id {category_id} not found"
            )
