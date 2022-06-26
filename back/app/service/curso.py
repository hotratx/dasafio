from app.api import CursoRepo
from app.schemas import CursosDB


class CursoService:
    def __init__(self, repo: CursoRepo):
        self._repo = repo

    async def get_all_curses(self):
        return await self._repo.get_all_curses()

    async def add_curso(self, data):
        curso = CursosDB(**data)
        return await self._repo.add_curso(curso)

    async def get_all_professores(self):
        return await self._repo.get_all_professores()

    async def get_all_alunos(self):
        return await self._repo.get_all_alunos()
