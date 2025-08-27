from uuid import UUID

from src.posts.repositories.create_post import CreatePost as CreatePostRepository
from src.posts.schemes.create_post_schema import CreatePostSchema


class CreatePost:
    def __init__(self, repository: CreatePostRepository):
        self.repository = repository

    async def create(self, data: CreatePostSchema, author_id: UUID) -> None:
        await self.repository.create(data, author_id)
