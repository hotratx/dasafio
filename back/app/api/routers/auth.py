from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.core.config import settings
from app.service.auth import AuthService, get_authenticated_user
from app.schemas import UserOut, UserInLogin
from app.core.user import UserModel
from .control_token import set_tokens_in_response, set_access_token_in_response

from dependency_injector.wiring import inject, Provide

from app.containers import Container


router = APIRouter()


@router.post("/register", response_model=UserOut)
@inject
async def register(
    request: Request,
    response: Response,
    auth: AuthService = Depends(Provide[Container.auth_service]),
    user: UserInLogin = Depends(get_authenticated_user),
):
    """
    register a new user
    Args:
        request: Request
        response: Response
    Returns:
        Response
    """
    await auth.only_staff(user)
    data = await request.json()
    user = await auth.register(data)
    return user


@router.post("/login", response_model=UserOut)
@inject
async def login(
    request: Request,
    response: Response,
    auth: AuthService = Depends(Provide[Container.auth_service]),
):

    """
    login a user
    Args:
        request (Request): Request
        response (Response): Response
    Returns:
        Response
    """
    data = await request.json()

    ip = request.client.host

    tokens, user = await auth.login(data, ip)
    set_tokens_in_response(response, tokens)
    return user


@router.post("/profile", response_model=UserOut)
@inject
async def update_profile(
    request: Request,
    response: Response,
    auth: AuthService = Depends(Provide[Container.auth_service]),
    user: UserInLogin = Depends(get_authenticated_user)
):

    """
    login a user
    Args:
        request (Request): Request
        response (Response): Response
    Returns:
        Response
    """
    data = await request.json()
    tokens, user = await auth.update_profile(data)
    set_tokens_in_response(response, tokens)
    return user


@router.post("/logout", response_model=UserOut)
async def logout(response: Response):
    """
    logout a user
    Args:
        response (Response): Response
    Returns:
        Response
    """
    response.delete_cookie(settings.access_cookie_name)
    response.delete_cookie(settings.refresh_cookie_name)
    return None


# @router.get("/me")
# async def me(user: UserModel = Depends(get_authenticated_user)):
#     """
#     Verify if request is authenticated
#     """
#     return {"Authenticated": user}


@router.get("/confirm", response_model=UserOut)
@inject
async def confirm_email(
    token: str, auth: AuthService = Depends(Provide[Container.auth_service])
):
    """
    confirm an email

    Args:
     token (str): token

    Returns:
     Response
    """
    return await auth.confirm_email(token)


@router.get("/refresh-token")
@inject
async def refresh_access_token(
    request: Request,
    response: Response,
    auth: AuthService = Depends(Provide[Container.auth_service]),
):
    """
    refresh an access token

    Args:
        request (Request): Request
        response (Response): Response

    Raises:
        HTTPException: HTTPException

    Returns:
        Response
    """
    refresh_token = request.cookies.get(settings.refresh_cookie_name)
    if refresh_token is None:
        raise HTTPException(401)

    access_token = await auth.refresh_access_token(refresh_token)
    set_access_token_in_response(response, access_token)
    return {"access": access_token}
