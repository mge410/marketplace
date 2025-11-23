from typing import List

from src.posts.repositories.get_list_of_posts import (
    GetListOfPosts as GetListOfPostsRepository,
)
from src.posts.schemes.post_query_schema import PostQuerySchema
from src.posts.schemes.posts_schema import PostSchema


class GetListOfPosts:
    def __init__(self, repository: GetListOfPostsRepository):
        self.repository = repository

    async def get_list_of_posts(
        self, filter_param: PostQuerySchema
    ) -> List[PostSchema]:
        posts = await self.repository.get_list_of_posts(filter_param)
        return [
            PostSchema(
                id=post.id,
                title=post.title,
                content=post.content,
                image_url=post.image_url,
                created_at=post.created_at,
                updated_at=post.updated_at,
                category_id=post.category_id,
                category_title=post.category.title,
            )
            for post in posts
        ]
