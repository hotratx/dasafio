from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session
from app.core.password import get_password_hash
from .database import User, Curso


async def create_user_staff():
    password = get_password_hash('12345')

    curso2 = Curso(
            nome="Python Avançado",
            professor='Manoel',
            ativo=True,
            data_inicio=datetime.utcnow(),
            data_termino=datetime.utcnow()+timedelta(days=30)
            )

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
            )

    curso1 = Curso(
            nome="Aprenda Python",
            professor='Manoel',
            ativo=True,
            data_inicio=datetime.utcnow(),
            data_termino=datetime.utcnow()+timedelta(days=90),
            users=[user_staff],
            )

    async with async_session() as session:
        session.add(curso2)
        session.add(curso1)
        await session.commit()
        await session.refresh(user_staff)
