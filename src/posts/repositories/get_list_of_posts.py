from abc import ABC, abstractmethod
from typing import Sequence

from src.core.database import PostModel


class GetListOfPosts(ABC):
    @abstractmethod
    async def get_list_of_posts(self) -> Sequence[PostModel]:
        pass
