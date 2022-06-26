from dependency_injector import containers, providers
from pydantic import BaseSettings

from app.api.deps import get_session
from app.api import UsersRepo, CursoRepo
from app.db.sqlmodel.model import CRUDUser, CRUDCurso
from app.cache import RedisBackend
from app.core import jwt
from app.service import auth, curso


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    class config:
        case_sensitive = True


settings = Settings()
url = settings.REDIS_HOST + "://" + settings.REDIS_HOST + ":" + settings.REDIS_PORT


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routers.auth",
            "app.api.routers.cursos"
            ]
    )

    redis = providers.Singleton(RedisBackend, "redis://redis:6379")
    session = providers.Resource(get_session)
    jwt = providers.Factory(jwt.JWTBackend, redis)

    crud_user = providers.Factory(CRUDUser)
    crud_curso = providers.Factory(CRUDCurso)

    repo_user = providers.Factory(
        UsersRepo, session=session, database=crud_user, cache=redis
    )
    repo_curso = providers.Factory(
        CursoRepo, session=session, database=crud_curso
    )

    auth_service = providers.Factory(auth.AuthService, jwt=jwt, repo=repo_user)
    curso_service = providers.Factory(curso.CursoService, repo=repo_curso)
