from fastapi import APIRouter, Depends, Request, Response

from app.service.curso import CursoService
from app.service.auth import AuthService, get_authenticated_user
from app.schemas import UserInLogin

from dependency_injector.wiring import inject, Provide
from app.containers import Container


router = APIRouter()


@router.post("/add_curso")
@inject
async def add_curso(
        request: Request,
        response: Response,
        auth: AuthService = Depends(Provide[Container.auth_service]),
        curso: CursoService = Depends(Provide[Container.curso_service]),
        user: UserInLogin = Depends(get_authenticated_user)):
    """
    register a new user
    Args:
        request: Request
        response: Response
    Returns:
        Response
    """
    await auth.only_staff(user)
    data = await request.json()
    resp = await curso.add_curso(data)
    return resp


@router.get("/professores")
@inject
async def get_professores(
        request: Request,
        response: Response,
        curso: CursoService = Depends(Provide[Container.curso_service])
        ):
    resp = await curso.get_all_professores()
    return resp 


@router.get("/alunos")
@inject
async def get_alunos(
        request: Request,
        response: Response,
        curso: CursoService = Depends(Provide[Container.curso_service])
        ):
    resp = await curso.get_all_alunos()
    return resp

@router.get("/cursos")
@inject
async def get_cursos(
        curso: CursoService = Depends(Provide[Container.curso_service])
        ):
    resp = await curso.get_all_cursos()
    return resp
