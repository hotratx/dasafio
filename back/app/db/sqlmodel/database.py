from typing import Optional, List
from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship


class CursoUserLink(SQLModel, table=True):
    curso_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="curso.id", primary_key=True
    )


# user = hero
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    sobrenome: Optional[str] = None
    email: str
    estado: Optional[str] = None
    cidade: Optional[str] = None
    endereco: Optional[str] = None
    tel_fixo: Optional[str] = None
    tel_movel: Optional[str] = None
    type_user: Optional[str] = None
    hashed_password: str
    cursos: List["Curso"] = Relationship(back_populates="users", link_model=CursoUserLink)


class Curso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    professor: str
    ativo: bool
    data_inicio: datetime
    data_termino: datetime
    users: List[User] = Relationship(back_populates="cursos", link_model=CursoUserLink)
