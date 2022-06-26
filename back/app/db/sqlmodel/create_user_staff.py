from .database import User, Cursos
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session
from app.core.password import get_password_hash


async def create_user_staff():
    password = get_password_hash('12345')

    curso2 = Cursos(
            nome="Python Avançado",
            professor='Manoel',
            alunos='euuu'
            )

    async with async_session() as session:
        session.add(curso2)
        await session.commit()
        session.refresh(curso2)

    user_staff = User(
            nome="admin",
            sobrenome="da Silva",
            email="admin@admin.com",
            estado="São Paulo",
            cidade="São Paulo",
            endereco="Rua da silveira, 224",
            tel_fixo=234234234,
            tel_movel=99999999,
            type_user="staff",
            hashed_password=password,
            cursos=[curso2]
            )

    async with async_session() as session:
        session.add(user_staff)
        await session.commit()
        session.refresh(user_staff)

    curso1 = Cursos(
            nome="Aprenda Python",
            professor='Manoel',
            alunos='euuu',
            user_id=user_staff.id
            )

    async with async_session() as session:
        session.add(curso1)
        await session.commit()
