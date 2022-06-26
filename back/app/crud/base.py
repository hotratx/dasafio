from typing import List, Protocol
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserDB, CursosDB


class BaseUser(Protocol):

    async def create(self, db: AsyncSession, obj_in: UserDB) -> UserDB:
        """Create new user"""
        ...

    async def get_by_email(self, db: AsyncSession, email: str):
        """Return user by email else raise"""
        ...

    async def all_users(self, db: AsyncSession) -> List[UserDB]:
        """Return all users"""
        ...

    async def update_profile(self, db: AsyncSession) -> List[UserDB]:
        """Return all users"""
        ...


class BaseCurso(Protocol):
    async def get_all_curses(self, db: AsyncSession):
        ...

    async def add_curso(self, db: AsyncSession, curso: CursosDB):
        ...

    async def get_all_professores(self, db: AsyncSession):
        ...

    async def get_all_alunos(self, db: AsyncSession):
        ...
