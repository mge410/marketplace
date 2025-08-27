from typing import Annotated, Any, List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.dependencies import get_current_user
from src.core.exceptions import UserNotFoundException
from src.core.schemes.user_scheme import UserSchema
from src.posts.exceptions.category_already_exists_exception import (
    CategoryAlreadyExistsException,
)
from src.posts.dependencies import (
    create_category_use_case,
    get_list_of_categories_use_case,
    get_list_of_posts_use_case,
    create_posts_use_case,
)
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.schemes.category_schema import CategorySchema
from src.posts.schemes.create_category_schema import CreateCategorySchema
from src.posts.schemes.create_post_schema import CreatePostSchema
from src.posts.schemes.posts_schema import PostSchema
from src.posts.use_cases.create_category import CreateCategory
from src.posts.use_cases.create_post import CreatePost
from src.posts.use_cases.get_list_of_categories import GetListOfCategories
from src.posts.use_cases.get_list_of_posts import GetListOfPosts

posts_router = APIRouter(
    tags=["posts"],
)

categories_router = APIRouter(
    tags=["categories"],
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
    try:
        await use_case.create_category(schema)

        return JSONResponse(
            content={"message": "Successfully created"},
            status_code=status.HTTP_201_CREATED,
        )
    except CategoryAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this title already exists",
        )


@categories_router.get("/posts", dependencies=[Depends(get_current_user)])
async def posts(
    use_case: Annotated[GetListOfPosts, Depends(get_list_of_posts_use_case)],
) -> List[PostSchema]:
    return await use_case.get_list_of_posts()


@categories_router.post("/posts", dependencies=[Depends(get_current_user)])
async def create_posts(
    data: CreatePostSchema,
    use_case: Annotated[CreatePost, Depends(create_posts_use_case)],
    user: Annotated[UserSchema, Depends(get_current_user)],
) -> JSONResponse:
    try:
        await use_case.create(data, user.uuid)

        return JSONResponse(
            content={"message": "Successfully created"},
            status_code=status.HTTP_201_CREATED,
        )
    except CategoryDoesNotExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Category not found"
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
