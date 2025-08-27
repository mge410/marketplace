from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    title: str
    content: str
    image_url: str
    category_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "cats post",
                "content": "cats post description",
                "image_url": "https://example.com/cat.jpg",
                "category_id": 1,
            }
        }
