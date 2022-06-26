from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from app.core.logger import logger
from sqlalchemy import update
from sqlmodel import select
from .database import User, Curso
from app.schemas import (
    UserDB, CursoDB, UserProfessor, UserUpdate, UserAlunos
)


class CRUDUser:
    _model = User

    async def create(self, db: AsyncSession, obj_in: UserDB) -> User:
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, email: str) -> User:
        resp = await db.execute(select(self._model).where(self._model.email == email))
        obj_out = resp.scalars().first()
        return obj_out

    async def all_users(self, db: AsyncSession) -> List[User]:
        resp = await db.execute(select(User))
        users = resp.scalars().all()
        response = [User.from_orm(user) for user in users]
        return response

    async def update_profile(self, db: AsyncSession, obj_in: UserUpdate) -> User:
        resp = await db.execute(select(self._model).where(self._model.email == obj_in.email))
        user = resp.scalars().first()
        logger.info(f"BUSCA DO USUARIO PARA UPDATE: {user}")
        user.nome = obj_in.nome
        user.sobrenome = obj_in.sobrenome
        user.email = obj_in.email
        user.estado = obj_in.estado
        user.cidade = obj_in.cidade
        user.endereco = obj_in.endereco
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


class CRUDCurso:
    _model = Curso

    async def create_new_curso(self, db: AsyncSession, obj_in: CursoDB) -> Curso:
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_all_curses(self, db: AsyncSession) -> List[Curso]:
        resp = await db.execute(select(Curso))
        users = resp.scalars().all()
        response = [Curso.from_orm(user) for user in users]
        return response

    async def add_curso(self, db: AsyncSession, obj_in: CursoDB) -> Curso:
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_all_professores(self, db: AsyncSession) -> List[UserProfessor]:
        resp = await db.execute(select(User).where(User.type_user == 'professor'))
        users = resp.scalars().all()
        response = [UserProfessor.from_orm(user) for user in users]
        return response

    async def get_all_alunos(self, db: AsyncSession) -> List[UserAlunos]:
        resp = await db.execute(select(User).where(User.type_user == 'aluno'))
        users = resp.scalars().all()
        response = [UserAlunos.from_orm(user) for user in users]
        return response

    async def get_all_cursos(self, db: AsyncSession) -> List[Curso]:
        resp = await db.execute(select(Curso))
        users = resp.scalars().all()
        response = [Curso.from_orm(user) for user in users]
        for u in response:
            logger.info(f"ALL CURSOSSSS: {u.users}")
        return response
