from typing import Dict, Tuple
from fastapi import HTTPException, Request
from pydantic.error_wrappers import ValidationError
from email_validator import EmailNotValidError, validate_email

from app.api import UsersRepo
from app.cache.redis import redis
from app.core.logger import logger
from app.core.jwt import JWTBackend
from app.core.email import EmailClient
from app.core.user import UserModel
from app.core.password import get_password_hash, verify_password
from app.core.config import settings
from app.resources.error_messages import get_error_message
from app.schemas import UserInRegister, UserInLogin, UserDB, UserUpdate

from app.utils.strings import create_random_string, hash_string


class AuthService:
    """Class AuthService, methods for login, logout, refresh, change password, change username
    This Class Depend on:
        - JWTBackend
        - UsersRepo
        - EmailClient
    """

    _base_url: str = settings.smtp_url
    _smtp_username: str = settings.smtp_username
    _smtp_host: str = settings.smtp_host
    _smtp_password: str = settings.smtp_password
    _smtp_tls: bool = settings.smtp_tls
    _site: str = "Bot Arbi"
    _display_name: str = "BotArb"

    def __init__(self, jwt: JWTBackend, repo: UsersRepo):
        self._auth_backend = jwt
        self._repo = repo

    def _create_email_client(self) -> EmailClient:
        return EmailClient(
            self._smtp_username,
            self._smtp_host,
            self._smtp_password,
            self._smtp_tls,
            self._base_url,
            self._site,
            self._display_name,
        )

    async def _request_email_confirmation(self, email: str) -> None:
        token = create_random_string()
        token_hash = hash_string(token)
        await self._repo.request_email_confirmation(email, token_hash)
        email_client = self._create_email_client()
        await email_client.send_confirmation_email(email, token)

    async def only_staff(self, staff_user: UserInLogin) -> bool:

        userdb = await self._repo.get_by_email(staff_user.email)

        if userdb is None:
            raise HTTPException(404)

        if userdb.type_user != 'staff':
            raise HTTPException(403, detail=get_error_message("only staff"))
        return True


    async def register(self, data: dict) -> UserDB:
        """POST /register
        Args:
            data: email, username, password1, password2.
        Returns:
            Access and refresh tokens.
        Raises:
            HTTPException:
                400 - validation error.
        """

        user = self._validate_user_model(UserInRegister, data)

        if await self._email_exists(user.email):
            raise HTTPException(400, detail=get_error_message("existing email"))

        # if await self._username_exists(user.username):
        #     raise HTTPException(400, detail=get_error_message("existing username"))

        new_user = UserDB(
            **user.dict(), hashed_password=get_password_hash(user.password)
        )

        try:
            validate_email(new_user.email, timeout=5)
        except EmailNotValidError:
            raise HTTPException(400, detail=get_error_message("try another email"))

        new_user_id = await self._repo.create(new_user)

        # return self._auth_backend.create_tokens(new_user_id.dict())
        return new_user_id

    async def update_profile(self, data: dict) -> Dict:
        try:
            user = UserUpdate(**data)
        except ValidationError:
            raise HTTPException(400)

        userdb = await self._repo.get_by_email(user.email)

        if userdb is None:
            raise HTTPException(404)

        userdb = await self._repo.update_profile(user)

        payload = userdb.dict(include={'nome', 'email', 'id'})
        token = self._auth_backend.create_tokens(payload)
        return token, userdb




    def _validate_user_model(self, model, data: dict):
        """
        Validate user model.
        Args:
            model (UserInRegister): schema model.
            data (dict): data.
        Raises:
            HTTPException: 400 - validation error.
        Returns:
            UserInRegister: UserInRegister model.
        """
        try:
            return model(**data)
        except ValidationError as e:
            msg = e.errors()[0].get("msg")
            raise HTTPException(400, detail=get_error_message(msg))

    async def _email_exists(self, email: str) -> bool:
        """
        Check if email exists.
        Args:
            email (str): email.
        Returns:
            bool: True if email exists.
        """
        return await self._repo.get_by_email(email) is not None

    async def _is_bruteforce(self, ip: str, login: str) -> bool:
        """
        Check if user is bruteforce.

        Args:
            ip (str): ip.
            login (str): login.

        Returns:
            bool: True if user is bruteforce.
        """
        return await self._repo.is_bruteforce(ip, login)

    async def login(self, data: dict, ip: str) -> Tuple:
        """POST /login
        Args:
            data: login, password.
            ip: for bruteforce check.
        Returns:
            Access and refresh tokens.
        Raises:
            HTTPException:
                400 - validation error or ban.
                404 - user doesn't exist.
                429 - bruteforce attempt.
        """
        try:
            user = UserInLogin(**data)
        except ValidationError:
            raise HTTPException(400)

        # if await self._is_bruteforce(ip, user.email):
        #     raise HTTPException(429, detail="Too many requests")

        userdb = await self._repo.get_by_email(user.email)

        if userdb is None:
            raise HTTPException(404)

        if not verify_password(user.password, userdb.hashed_password):
            raise HTTPException(401, detail="credential invalid")

        # await self._update_last_login(user.get("id"))

        payload = userdb.dict(include={'nome', 'email', 'id'})
        logger.info(f"DATABASE COMPLETO {payload}")
        # payload = user.dict()
        token = self._auth_backend.create_tokens(payload)
        return token, userdb

    async def confirm_email(self, token: str):
        """POST /confirm/{token}

        Hashes token, looks up hash in db, updates "confirmed" to True for email in a row.

        Raises:
         HTTPException:
             403 - no hash in db.
        """
        token_hash = hash_string(token)
        user = await self._repo.confirm_email(token_hash)
        if user:
            return user
        raise HTTPException(403)

    async def refresh_access_token(self, refresh_token: str) -> str:
        """POST /token/refresh

        Args:
            refresh_token: refresh_token from cookies.

        Returns:
            Access token.

        Raises:
            HTTPException:
                401 - type != refresh or ban.
                500 - ttt
        """
        refresh_token_payload = await self._auth_backend.decode_token(refresh_token)
        if (
            refresh_token_payload is None
            or refresh_token_payload.get("type") != "refresh"
        ):
            raise HTTPException(401)

        item = await self._repo.get_by_email(refresh_token_payload.get("email"))
        if item is None:
            raise HTTPException(401)

        payload = item.dict(include={'username', 'email', 'id'})
        return self._auth_backend.create_access_token(payload)


async def get_authenticated_user(request: Request) -> UserModel:
    access_token = request.cookies.get(settings.access_cookie_name)
    logger.info(f"access_token: {access_token}")
    if access_token:
        jwt = JWTBackend(redis)
        return await UserModel.create(access_token, jwt)
    else:
        raise HTTPException(401)


async def admin_required(self, request: Request) -> None:
    access_token = request.cookies.get(self._access_cookie_name)
    if access_token:
        user = await UserModel.create(access_token, self._auth_backend)
        if user.is_admin:
            return
    raise HTTPException(403)
