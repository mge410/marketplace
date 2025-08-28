from abc import ABC, abstractmethod
from uuid import UUID

from src.core.database import PostModel
from src.posts.schemes.update_post_schema import UpdatePostSchema


class UpdatePost(ABC):
    @abstractmethod
    async def update(
        self, post_id: int, data: UpdatePostSchema, author_id: UUID
    ) -> PostModel | None:
        pass
