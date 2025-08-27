from abc import ABC, abstractmethod
from typing import Sequence

from src.core.database import CategoryModel


class GetListOfCategories(ABC):
    @abstractmethod
    async def get_list_of_categories(self) -> Sequence[CategoryModel]:
        pass
