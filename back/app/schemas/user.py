from typing import Optional, List
from fastapi import HTTPException
from app.resources.error_messages import get_error_message
from enum import Enum

from pydantic import EmailStr, BaseModel, validator
from app.schemas.base import BaseSchema

"""
Preciso colocar condições nos campos, como tamanho mínimo de senha
e username.
"""


class TypeUser(Enum):
    STAFF = 1
    PROF = 2
    ALUNO = 3


class UserDB(BaseSchema):
    id: Optional[int] = None
    nome: str
    type_user: str
    hashed_password: str
    sobrenome: Optional[str] = ""
    email: Optional[EmailStr | None] = None
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    endereco: Optional[str] = ""
    tel_fixo: Optional[int] = 0
    tel_movel: Optional[int] = 0


class UserUpdate(BaseSchema):
    nome: str
    sobrenome: Optional[str] = ""
    email: Optional[EmailStr | None] = None
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    endereco: Optional[str] = ""
    tel_fixo: Optional[int] = 0
    tel_movel: Optional[int] = 0


class UserOut(BaseSchema):
    nome: str
    type_user: str
    sobrenome: Optional[str] = ""
    email: Optional[EmailStr | None] = None
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    endereco: Optional[str] = ""
    tel_fixo: Optional[int] = 0
    tel_movel: Optional[int] = 0


class UserInRegister(BaseModel):
    nome: str
    email: EmailStr
    type_user: str
    password: str

    @validator('type_user')
    def type_of_users(cls, v):
        if v not in ['staff', 'professor', 'aluno']:
            raise HTTPException(400, detail=get_error_message("user wrong"))
        return v


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfessor(BaseSchema):
    nome: str
    type_user: str
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    email: Optional[EmailStr | None] = None
    tel_fixo: Optional[int] = 0
    tel_movel: Optional[int] = 0

class UserAlunos(BaseSchema):
    nome: str
    type_user: str
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    email: Optional[EmailStr | None] = None
    tel_fixo: Optional[int] = 0
    tel_movel: Optional[int] = 0
