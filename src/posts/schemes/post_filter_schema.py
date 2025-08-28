from typing import Optional

from pydantic import Field


class PostFilterSchema:
    search: Optional[str] = Field(None, description="Full-text search query")
    category_id: Optional[int] = Field(None, description="Filter by category ID")
