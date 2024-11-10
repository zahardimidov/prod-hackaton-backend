import asyncio

import pytest
from httpx import AsyncClient
from run import app


# @pytest.mark.asyncio
# async def test_read_main():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         response = await ac.post("/auth/register", json={"username": "USERNAME15", "password": "aa22aa22"})
#         assert response.status_code == 200
#         assert response.json() == {"detail": "Successfully registered"}
#

#
# @pytest.mark.asyncio
# async def test_auth_register_user_already():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         response = await ac.post("/auth/register", json={"username": "USERNAME1", "password": "aa22aa22"})
#         assert response.status_code == 400
#         assert response.json() == {"detail": "This username is already taken"}
#
#
# @pytest.mark.asyncio
# async def test_auth_register_username_small():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as conn:
#         response = await conn.post("/auth/register", json={"username": "test", "password": "aa22aa22"})
#         assert response.status_code == 422
#
#
# @pytest.mark.asyncio
# async def test_auth_register_password_without_nums():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as conn:
#         response = await conn.post("/auth/register", json={"username": "testusername", "password": "aaaaaaa"})
#         assert response.status_code == 400
#         assert response.json() == {"detail": "Password must include numbers"}
#
#
# @pytest.mark.asyncio
# async def test_auth_register_password_small():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as conn:
#         response = await conn.post("/auth/register", json={"username": "testusername", "password": "aa22"})
#         assert response.status_code == 422

@pytest.fixture
async def token():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as conn:
        response = await conn.post("/auth/login", json={"username": "USERNAME15", "password": "aa22aa22"})
        return response.json()["access_token"]


@pytest.mark.asyncio
async def test_group_create_equal():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/group/create_equal", headers={"Authorization": f"Bearer {token}"}, json={
            "title": "test",
            "price": 2000
        })
        assert response.status_code == 200
