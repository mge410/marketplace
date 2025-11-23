from abc import ABC, abstractmethod
from uuid import UUID


class DeletePost(ABC):
    @abstractmethod
    async def delete(self, post_id: int, user_id: UUID) -> None:
        pass
