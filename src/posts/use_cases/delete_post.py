from uuid import UUID

from src.posts.repositories.delete_post import DeletePost as DeletePostRepository


class DeletePost:
    def __init__(self, repository: DeletePostRepository):
        self.repository = repository

    async def delete(self, post_id: int, user_id: UUID) -> None:
        await self.repository.delete(post_id, user_id)
