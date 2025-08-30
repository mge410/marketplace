from pydantic import Field, BaseModel, ConfigDict


class CategorySchema(BaseModel):
    id: int
    title: str = Field(
        description="Имя категории (2-25 символов)", min_length=2, max_length=25
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "cats category",
            }
        }
    )
