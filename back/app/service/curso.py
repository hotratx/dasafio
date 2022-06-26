from app.api import CursoRepo
from app.schemas import CursoDB
from app.core.logger import logger
from datetime import datetime


class CursoService:
    def __init__(self, repo: CursoRepo):
        self._repo = repo

    async def get_all_curses(self):
        return await self._repo.get_all_curses()

    async def add_curso(self, data):
        data['data_inicio'] = datetime.strptime(data['data_inicio'], "%Y-%m-%d")
        data['data_termino'] = datetime.strptime(data['data_termino'], "%Y-%m-%d")
        curso = CursoDB(**data)
        return await self._repo.add_curso(curso)

    async def get_all_professores(self):
        return await self._repo.get_all_professores()

    async def get_all_alunos(self):
        return await self._repo.get_all_alunos()

    async def get_all_cursos(self):
        return await self._repo.get_all_cursos()
