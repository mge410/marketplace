from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    image_url: str
    created_at: datetime
    updated_at: datetime
    category_id: int
    category_title: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "cats post",
                "content": "cats post description",
                "image_url": "https://example.com/cat.jpg",
                "created_at": datetime(2020, 1, 1),
                "updated_at": datetime(2020, 1, 1),
                "category_id": 1,
                "category_title": "cats",
            }
        }
