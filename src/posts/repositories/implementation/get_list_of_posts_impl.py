from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.database import PostModel
from src.posts.repositories.get_list_of_posts import GetListOfPosts


class GetListOfPostsImpl(GetListOfPosts):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list_of_posts(self) -> Sequence[PostModel]:
        query = select(PostModel).options(selectinload(PostModel.category))
        result = await self.session.execute(query)
        posts = result.scalars().unique().all()
        return posts
