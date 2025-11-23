from pydantic import BaseModel, ConfigDict


class CreatePostSchema(BaseModel):
    title: str
    content: str
    image_url: str
    category_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "cats post",
                "content": "cats post description",
                "image_url": "https://example.com/cat.jpg",
                "category_id": 1,
            }
        }
    )
