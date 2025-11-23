from typing import Any

from sqlalchemy.sql.selectable import Select

from src.posts.schemes.post_paginate_schema import PostPaginateSchema


class PostPaginateMixin:
    @staticmethod
    async def paginate(query: Select[Any], data: PostPaginateSchema) -> Select[Any]:
        offset = (data.page_number - 1) * data.page_size
        return query.offset(offset).limit(data.page_size)
