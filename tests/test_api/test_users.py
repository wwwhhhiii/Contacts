import pytest
from httpx import AsyncClient

from ..conftest import create_user, get_access_token
from .. import model_generator


@pytest.mark.usefixtures("create_tables")
class TestLogin:

    @pytest.mark.asyncio
    async def test_login_401(self, client: AsyncClient):
        username = 'foo1'
        password = '123'
        user = await create_user(username=username, password=password)
        data = {
            'username': username,
            'password': 'invalid',
        }

        response = await client.post(url="/auth/token", data=data)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_200(self, client: AsyncClient):
        username = 'foo2'
        password = '123'
        user = await create_user(username=username, password=password)
        data = {
            'username': username,
            'password': password,
        }

        response = await client.post(url="/auth/token", data=data)
        assert response.status_code == 200


@pytest.mark.usefixtures("create_tables")
class TestRegister:
    @pytest.mark.asyncio
    async def test_duplicate_id(self, client: AsyncClient):
        existing_user = await create_user()
        user = model_generator.User()
        user.id = existing_user.id
        json = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
        }

        response = await client.post(url="/users/register", json=json)
        assert response.status_code == 409
        assert "id already exist" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_duplicate_username(self, client: AsyncClient):
        existing_user = await create_user()
        user = model_generator.User()
        user.username = existing_user.username
        json = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
        }

        response = await client.post(url="/users/register", json=json)
        assert response.status_code == 409
        assert "username already exist" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_201(self, client: AsyncClient):
        user = model_generator.User()
        json = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
        }

        response = await client.post(url="/users/register", json=json)
        assert response.status_code == 201


@pytest.mark.usefixtures("create_tables")
class TestGet:
    @pytest.mark.asyncio
    async def test_get_me(self, client: AsyncClient):
        user = await create_user()
        token = await get_access_token(username=user.username, password=user.password)

        headers = {
            "Authorization": "Bearer " + token,
        }

        response = await client.get(url="/users/me", headers=headers)
        assert response.status_code == 200
