from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import PostModel, UserModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.post_not_found_exception import PostNotFoundException
from src.posts.exceptions.user_has_no_access_exception import UserHasNoAccessException


class PostAccessMixin:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _find_post_by_id(self, post_id: int) -> PostModel:
        query = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.execute(query)
        try:
            post = result.scalar_one()
        except NoResultFound:
            raise PostNotFoundException(f"Post with id {post_id} not found")
        return post

    async def _check_author_access(self, post: PostModel, user_id: UUID) -> None:
        query = select(UserModel).where(UserModel.uuid == user_id)
        result = await self.session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException()

        if post.author_id != user.id:
            raise UserHasNoAccessException()
