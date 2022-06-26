from typing import List, Dict
from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.logger import logger
from app.service.curso import CursoService
from app.service.auth import AuthService, get_authenticated_user
from app.schemas import UserInLogin
from .control_token import set_tokens_in_response, set_access_token_in_response

from dependency_injector.wiring import inject, Provide
from app.containers import Container


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
@inject
async def start_page(
        request: Request,
        curso: CursoService = Depends(Provide[Container.curso_service])
        ):

    all_cursos = await curso.get_all_curses()
    logger.info(f"all cursos: {all_cursos}")
    return templates.TemplateResponse("index.html", {"request": request, "id": all_cursos})


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
