from typing import Optional
from datetime import datetime

from app.schemas.base import BaseSchema


class CursoDB(BaseSchema):
    id: Optional[int] = None
    nome: str
    professor: str
    ativo: bool
    data_inicio: datetime
    data_termino: datetime
