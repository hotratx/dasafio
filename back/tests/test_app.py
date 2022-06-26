import pytest
import httpx
from fastapi import status


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"foi": 18}

@pytest.mark.asyncio
class TestCreatePerson:
    async def test_invalid(self, test_client: httpx.AsyncClient):
        payload = {"name": "Maria", "email": "maria@gmail.com"}
        response = await test_client.post("/auth/signup", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, test_client: httpx.AsyncClient):
        payload = {"name": "Maria", "email": "maria@gmail.com", "password": "12345"}
        response = await test_client.post("/auth/signup", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        #assert json == payload
