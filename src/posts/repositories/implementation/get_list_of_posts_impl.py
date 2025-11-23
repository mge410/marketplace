from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.database import PostModel
from src.posts.repositories.get_list_of_posts import GetListOfPosts
from src.posts.repositories.implementation.mixins.post_filter_mixin import (
    PostFilterMixin,
)
from src.posts.repositories.implementation.mixins.post_paginate_mixin import (
    PostPaginateMixin,
)
from src.posts.schemes.post_query_schema import PostQuerySchema


class GetListOfPostsImpl(GetListOfPosts, PostFilterMixin, PostPaginateMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session

    async def get_list_of_posts(
        self, filter_param: PostQuerySchema
    ) -> Sequence[PostModel]:
        query = select(PostModel).options(selectinload(PostModel.category))
        query = await self.filter(query, filter_param)
        query = await self.paginate(query, filter_param)
        result = await self.session.execute(query)
        posts = result.scalars().unique().all()
        return posts
