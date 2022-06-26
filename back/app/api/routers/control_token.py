from typing import Dict
from fastapi import Response
from app.core.config import settings


def set_access_token_in_response(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.access_cookie_name,
        value=token,
        secure=False,
        httponly=True,
        expires=6000,
        max_age=6000,
    )


def set_refresh_token_in_response(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=token,
        secure=False,
        httponly=True,
        expires=12000,
        max_age=12000,
    )


def set_tokens_in_response(response, tokens: Dict[str, str]) -> None:
    access_token = tokens.get("access")
    refresh_token = tokens.get("refresh")
    set_access_token_in_response(response, access_token)
    set_refresh_token_in_response(response, refresh_token)

