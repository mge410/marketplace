from abc import ABC, abstractmethod
from typing import Sequence

from src.core.database import PostModel
from src.posts.schemes.post_query_schema import PostQuerySchema


class GetListOfPosts(ABC):
    @abstractmethod
    async def get_list_of_posts(
        self, filter_param: PostQuerySchema
    ) -> Sequence[PostModel]:
        pass
