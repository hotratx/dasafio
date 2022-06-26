from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jwt import JWTBackend
from app.core.user import UserModel
from app.core.config import settings
from app.db import async_session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_authenticated_user(
     request: Request,
 ) -> UserModel:
    access_token = request.cookies.get(settings.access_cookie_name)
    if access_token:
        jwt = JWTBackend()
        return await UserModel.create(access_token, jwt)
    else:
        raise HTTPException(401)
