from typing import Annotated, Any

from fastapi import APIRouter
from fastapi.params import Depends

from src.posts.dependencies import create_category_use_case
from src.posts.schemes.create_category_schema import CreateCategorySchema
from src.posts.use_cases.create_category import CreateCategory

posts_router = APIRouter(
    tags=["posts"],
)

categories_router = APIRouter(
    tags=["categories posts"],
)


@categories_router.post("/categories")
async def categories(
    schema: CreateCategorySchema,
    use_case: Annotated[CreateCategory, Depends(create_category_use_case)],
) -> Any:
    use_case.create_category(schema)

    return {"success": True}
