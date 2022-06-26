from typing import Optional

#from email_validator import EmailNotValidError, validate_email

from app.core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.cache import RedisBackend
from app.core.logger import logger
from app.crud import BaseUser
from app.schemas import UserOut, UserDB, UserUpdate
from app.core.config import settings


class Base:
    """
    Initialize the API with the database and cache.
    """

    def __init__(
        self,
        session: AsyncSession,
        database: BaseUser, # poderá ser um dict com values talbes user, movie
        cache: RedisBackend,
    ):
        """Initialize the API with the database and cache.

        Args:
            database (MongoDBBackend): The database to use.
            cache (RedisBackend): The cache to use.
            callbacks (Iterable): The callbacks to use.
            access_expiration (int, optional): The expiration time for access tokens. Defaults to 60 * 60 * 6.
        """
        self._session = session
        self._database = database
        self._cache = cache


class UsersCRUDMixin(Base):
    """User CRUD MIXIN

    Args:
    Create all the Common CRUDS GET, POST, PUT, DELETE methods.
    """
    async def get_by_email(self, email: str) -> UserDB | None:
        """
        Get a user by email.

        Args:
         email (str): The email of the user.

        Returns:
         Optional[dict]: The user.
        """
        try:
            user = await self._database.get_by_email(self._session, email)
            return UserDB.from_orm(user)
        except:
            return None

    async def create(self, obj: UserDB) -> Optional[UserDB]:
        """
        Create a user.

        Args:
            obj (dict): The user to create.

        Returns:
            int: The id of the user.
        """
        return await self._database.create(self._session, obj)

    async def update_profile(self, obj: UserUpdate) -> Optional[UserDB]:
        """
        Create a user.

        Args:
            obj (dict): The user to create.

        Returns:
            int: The id of the user.
        """
        return await self._database.update_profile(self._session, obj)

class UsersConfirmMixin(Base):
    """User Confirmation MIXIN

    Args:
        Create all the Common Confirmation GET, POST, PUT, DELETE methods.
    """

    async def request_email_confirmation(self, email: str, token_hash: str) -> None:
        """
        Request an email confirmation.

        Args:
            email (str): The email of the user.
            token_hash (str): The token hash.

        Returns:
            None
        """
        await self._database.request_email_confirmation(self._session, email, token_hash)
        return None

    async def confirm_email(self, token_hash: str) -> Optional[UserOut]:
        """
        Confirm an email.

        Args:
            token_hash (str): The token hash.

        Returns:
            bool: True if the email is confirmed.
        """
        return await self._database.confirm_email(self._session, token_hash)


class UsersProtectionMixin(Base):
    """User Protection MIXIN

    Args:
     Create all the Common Protection GET, POST, PUT, DELETE methods.
    """
    async def is_bruteforce(self, ip: str, login: str) -> bool:
        """
        Check if the ip is in the bruteforce list.

        Args:
            ip (str): The ip to check.
            login (str): The login to check.

        Returns:
            bool: True if the ip is in the bruteforce list.
        """
        timeout_key = f"users:login:timeout:{ip}"
        timeout = await self._cache.get(timeout_key)

        if timeout is not None:
            return True  # pragma: no cover

        rate_key = f"users:login:rate:{ip}"
        rate = await self._cache.get(rate_key)
        logger.info(f"------------- users:login:rate = {rate}")

        if rate is not None:
            rate = int(rate)  # pragma: no cover
            if rate > settings.login_ratelimit:  # pragma: no cover
                await self._cache.set(timeout_key, 1, ex=60)  # pragma: no cover     ■ "set" is not a known member of "None"
                logger.info(
                    f"bruteforce_login ip={ip} login={login}"
                )  # pragma: no cover
                return True  # pragma: no cover
        else:
            await self._cache.set(rate_key, 1, ex=60)

        await self._cache.incr(rate_key)
        return False

class UsersManagementMixin(Base):
    """User Management MIXIN

    Args:
        Create all the Common Management GET, POST, PUT, DELETE methods.
    """
    async def search_blacklist(self, token) -> bool:
        user_blacklist = await self._cache.get(f"users:blacklist:{token}")
        if user_blacklist:
            return True
        return False



class UsersRepo(
    UsersCRUDMixin,
    UsersConfirmMixin,
    # UsersPasswordMixin,
    # UsersUsernameMixin,
    UsersProtectionMixin,
    UsersManagementMixin,
):
    """User Repository

    Args:
        UsersCRUDMixin: CRUD methods
        UsersConfirmMixin: Confirmation methods
        UsersPasswordMixin: Password methods
        UsersUsernameMixin: Username methods
        UsersProtectionMixin: Protection methods
        UsersManagementMixin: Management methods
    """

#users_repo = UsersRepo(user, redis)
