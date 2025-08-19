from typing import Annotated

from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from starlette import status

from src.auth.dependencies.register import register_service, login_service
from src.auth.exceptions.IncorrectPasswordException import IncorrectPasswordException
from src.auth.exceptions.MultipleValidationException import MultipleValidationException
from src.auth.exceptions.UserNotFoundException import UserNotFoundException
from src.auth.schemes.login_user import LoginUserSchema, TokenInfo
from src.auth.schemes.register_user import RegisterUserSchema
from src.auth.services.login import LoginService
from src.auth.services.register import RegisterService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register")
async def register(
        user: RegisterUserSchema,
        service: Annotated[RegisterService, Depends(register_service)],
        response: Response
) -> dict[str, bool]:
    try:
        token_info = await service.register_user(user)

        response.set_cookie(
            key="access_token",
            value=f"{token_info.token_type} {token_info.token}",
            max_age=token_info.max_age,
            httponly=True,
            secure=True,
            samesite="lax"
        )

    except MultipleValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.to_response())

    return {"success": True}


@router.post("/login")
async def login(
    user: LoginUserSchema,
    service: Annotated[LoginService, Depends(login_service)],
    response: Response
) -> TokenInfo:
    try:
        token_info = await service.login(user)
        response.set_cookie(
            key="access_token",
            value=f"{token_info.token_type} {token_info.token}",
            max_age=token_info.max_age,
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return token_info

    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except IncorrectPasswordException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")



@router.post("/logout")
async def logout():
    return {"message": "Hello Logout"}
