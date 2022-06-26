from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import BaseCurso
from app.schemas import CursoDB, UserProfessor, UserAlunos
from app.core.logger import logger


class CursoRepo:
    def __init__(self, session: AsyncSession, database: BaseCurso):
        self._session = session
        self._database = database

    async def get_all_curses(self):
        try:
            user = await self._database.get_all_curses(self._session)
            return user
        except:
            return 'erro'

    async def add_curso(self, curso: CursoDB):
        return await self._database.add_curso(self._session, curso)

    async def get_all_professores(self) -> UserProfessor | None:
        profs = await self._database.get_all_professores(self._session)
        logger.info(f"PROFESSORES: {profs}")
        return profs

    async def get_all_alunos(self) -> UserAlunos | None:
        alunos = await self._database.get_all_alunos(self._session)
        logger.info(f"ALUNOS: {alunos}")
        return alunos

    async def get_all_cursos(self) -> UserAlunos | None:
        cursos = await self._database.get_all_cursos(self._session)
        logger.info(f"CURSOS: {cursos}")
        return cursos
