from dataclasses import dataclass
from src.core.database.models.post_model import PostModel
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class CreatePostData:
    title: str
    content: str
    image_url: str
    category_id: int
    author_id: int


class PostBuilder:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def build(self, data: CreatePostData) -> PostModel:
        model = self._build_post(data)
        await self._save_post(model)
        return model

    @staticmethod
    def _build_post(data: CreatePostData) -> PostModel:
        return PostModel(
            title=data.title,
            content=data.content,
            image_url=data.image_url,
            category_id=data.category_id,
            author_id=data.author_id,
        )

    async def _save_post(self, post: PostModel) -> None:
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
