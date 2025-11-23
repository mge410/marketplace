from src.posts.schemes.post_filter_schema import PostFilterSchema
from src.posts.schemes.post_paginate_schema import PostPaginateSchema


class PostQuerySchema(PostPaginateSchema, PostFilterSchema):
    pass
