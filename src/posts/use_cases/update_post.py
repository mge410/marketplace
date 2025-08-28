from uuid import UUID

from src.posts.repositories.update_post import UpdatePost as UpdatePostRepository
from src.posts.schemes.update_post_schema import UpdatePostSchema


class UpdatePost:
    def __init__(self, repository: UpdatePostRepository):
        self.repository = repository

    async def update(
        self, post_id: int, data: UpdatePostSchema, author_id: UUID
    ) -> None:
        await self.repository.update(post_id=post_id, data=data, author_id=author_id)
