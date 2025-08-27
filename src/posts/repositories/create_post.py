from abc import ABC, abstractmethod
from uuid import UUID

from src.core.database import PostModel
from src.posts.schemes.create_post_schema import CreatePostSchema


class CreatePost(ABC):
    @abstractmethod
    async def create(self, data: CreatePostSchema, author_id: UUID) -> PostModel | None:
        pass
