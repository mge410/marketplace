from typing import Any, Optional

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from src.core.database import PostModel
from src.posts.schemes.post_filter_schema import PostFilterSchema


class PostFilterMixin:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def filter(self, query: Select[Any], data: PostFilterSchema) -> Select[Any]:
        await self.__filter_by_category(query, data.category_id)
        await self.__filter_by_search(query, data.search)
        return query

    @staticmethod
    async def __filter_by_category(
        query: Select[Any], category_id: Optional[int]
    ) -> Select[Any]:
        if category_id:
            query = query.where(PostModel.category_id == category_id)
        return query

    @staticmethod
    async def __filter_by_search(
        query: Select[Any], search: Optional[str]
    ) -> Select[Any]:
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    PostModel.title.ilike(search_pattern),
                    PostModel.content.ilike(search_pattern),
                )
            )
        return query
