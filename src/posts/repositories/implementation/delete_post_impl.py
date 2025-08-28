from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import PostModel, UserModel
from src.core.database.models.deleted_post_model import DeletedPostModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.post_not_found_exception import PostNotFoundException
from src.posts.exceptions.user_has_no_access_exception import UserHasNoAccessException
from src.posts.repositories.delete_post import DeletePost


class DeletePostImpl(DeletePost):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, post_id: int, user_id: UUID) -> None:
        post = await self._find_post_by_id(post_id)
        await self._check_that_user_has_access(post, user_id)

        deleted_post = DeletedPostModel(
            title=post.title,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            category_id=post.category_id,
            author_id=post.author_id,
            deleted_at=datetime.now(timezone.utc),
        )

        await self.session.delete(post)
        self.session.add(deleted_post)
        await self.session.commit()

    async def _find_post_by_id(self, post_id: int) -> PostModel:
        query = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.execute(query)
        try:
            post = result.scalar_one()
        except NoResultFound:
            raise PostNotFoundException(f"Post with id {post_id} not found")
        return post

    async def _check_that_user_has_access(self, post: PostModel, user_id: UUID) -> None:
        query = select(UserModel).where(UserModel.uuid == user_id)
        result = await self.session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException()

        if post.author_id != user.id:
            raise UserHasNoAccessException()
