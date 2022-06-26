import pytest
import asyncio 
from asgi_lifespan import LifespanManager
import httpx

from app.main import app
from app.models.user import User
from app.db.base_class import Base
from app.api.deps import get_session


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@db:5432/foo", echo=True, future=True)
async_session = sessionmaker(
                        engine,
                        class_=AsyncSession,
                        expire_on_commit=False
                )

async def get_test_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_client():
    app.dependency_overrides[get_session] = get_test_session
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app,
                base_url="http://app.io") as test_client:
            yield test_client

#@pytest.fixture(autouse=True, scope="module")
#async def initial_posts():
#    session = get_test_session()
#    initial_posts = User(name="Jose 1", email="ee@gmail.com", cidade="farroupilha" , hashed_password="12345")
#    await session.add(initial_posts)
#    yield initial_posts
