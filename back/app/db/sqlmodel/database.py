from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


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
    cursos: List["Cursos"] = Relationship(back_populates="user")


class Cursos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    professor: str
    alunos: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="cursos")
