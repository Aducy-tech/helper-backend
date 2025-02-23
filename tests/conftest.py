from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from src.main import app
from src.core.config import settings
from src.database.database import engine
from src.database.models import Base
from src.schemas import user_schema, token_schema
from src.utils.auth_utils import decode_jwt


@fixture(loop_scope='session', autouse=True)
async def setup_db():
    assert settings.database_settings.MODE == 'TEST'

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@fixture(loop_scope='session')
async def registered_client(setup_db) -> (
    AsyncGenerator[user_schema.UserCreate, None]
):
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        user_in = user_schema.UserCreate(
            username='John',
            email='user@example.ru',
            password='12345'
        )
        response = await ac.post(
            '/users/register/',
            json=user_in.model_dump()
        )
        assert response.status_code == 201
        yield user_in


@fixture(loop_scope='session')
async def logined_user(registered_client) -> (
    AsyncGenerator[token_schema.TokenResponse, None]
):
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        user_data = registered_client
        response = await ac.post(
            '/users/login/',
            json=user_data.model_dump()
        )

        assert response.status_code == 200
        yield token_schema.TokenResponse.model_validate(response.json())


@fixture(loop_scope='session')
async def access_token(logined_user) -> str:
    return logined_user.access_token


@fixture(loop_scope='session')
async def user_payload(logined_user) -> AsyncGenerator[dict, None]:
    yield decode_jwt(logined_user.access_token)
