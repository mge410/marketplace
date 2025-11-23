from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    image_url: str
    created_at: datetime
    updated_at: datetime
    category_id: int
    category_title: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "cats post",
                "content": "cats post description",
                "image_url": "https://example.com/cat.jpg",
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
                "category_id": 1,
                "category_title": "cats",
            }
        }
    )
