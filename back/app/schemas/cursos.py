from typing import Optional

from app.schemas.base import BaseSchema


class CursosDB(BaseSchema):
    id: Optional[int] = None
    nome: str
    professor: str
    alunos: Optional[str]
    user_id: int
