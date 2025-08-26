from typing import Annotated

from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.auth.dependencies import register_use_case, login_use_case
from src.auth.exceptions.IncorrectPasswordException import IncorrectPasswordException
from src.auth.exceptions.MultipleValidationException import MultipleValidationException
from src.auth.exceptions.UserNotFoundException import UserNotFoundException
from src.auth.schemes.login_user import LoginUserSchema, TokenInfo
from src.auth.schemes.register_user import RegisterUserSchema
from src.auth.use_cases.login import LoginUseCase
from src.auth.use_cases.register import RegisterUseCase

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: RegisterUserSchema,
    use_case: Annotated[RegisterUseCase, Depends(register_use_case)],
    response: Response,
) -> dict[str, bool]:
    try:
        token_info = await use_case.register_user(user)
        await set_access_cookie(response, token_info)

        return {"success": True}

    except MultipleValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.to_response()
        )


@router.post("/login")
async def login(
    user: LoginUserSchema,
    use_case: Annotated[LoginUseCase, Depends(login_use_case)],
    response: Response,
) -> TokenInfo:
    try:
        token_info = await use_case.login(user)
        await set_access_cookie(response, token_info)

        return token_info

    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except IncorrectPasswordException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )


@router.post("/logout")
async def logout(response: Response) -> JSONResponse:
    response.delete_cookie(
        key="access_token",
        path="/",
        domain=None,
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return JSONResponse(
        content={"message": "Successfully logged out"}, status_code=status.HTTP_200_OK
    )


async def set_access_cookie(response: Response, token_info: TokenInfo) -> None:
    response.set_cookie(
        key="access_token",
        value=f"{token_info.token_type} {token_info.token}",
        max_age=token_info.max_age,
        httponly=True,
        secure=True,
        samesite="lax",
    )
