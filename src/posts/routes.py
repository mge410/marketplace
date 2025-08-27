from typing import Annotated, Any, List

from fastapi import APIRouter
from fastapi.params import Depends

from src.core.dependencies import get_current_user
from src.posts.dependencies import create_category_use_case, get_list_of_categories_use_case
from src.posts.schemes.category_schema import CategorySchema
from src.posts.schemes.create_category_schema import CreateCategorySchema
from src.posts.use_cases.create_category import CreateCategory
from src.posts.use_cases.get_list_of_categories import GetListOfCategories

posts_router = APIRouter(
    tags=["posts"],
)

categories_router = APIRouter(
    tags=["categories posts"],
)

@categories_router.get("/categories", dependencies=[Depends(get_current_user)])
async def categories(
    use_case: Annotated[GetListOfCategories, Depends(get_list_of_categories_use_case)],
) -> List[CategorySchema]:
    return await use_case.get_list_of_category()

@categories_router.post("/categories", dependencies=[Depends(get_current_user)])
async def create_category(
    schema: CreateCategorySchema,
    use_case: Annotated[CreateCategory, Depends(create_category_use_case)],
) -> Any:
    await use_case.create_category(schema)

    return {"success": True}
