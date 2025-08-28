from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.deleted_post_model import DeletedPostModel
from src.posts.repositories.delete_post import DeletePost
from src.posts.repositories.implementation.mixins.post_access_mixin import PostAccessMixin


class DeletePostImpl(DeletePost, PostAccessMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session

    async def delete(self, post_id: int, user_id: UUID) -> None:
        post = await self._find_post_by_id(post_id)
        await self._check_author_access(post, user_id)

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
