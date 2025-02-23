import pytest

from httpx import AsyncClient, ASGITransport
from src.main import app
from src.schemas import ai_schema
from src.core.config import settings


@pytest.mark.asyncio(loop_scope='session')
async def test_get_minimum_tokens_for_ai():
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get(
            '/ai/minimum-tokens-for-ai/',
        )

        assert response.status_code == 200
        expected = ai_schema.MinimumTokensForAIResponse(
            tokens=settings.ai.min_tokens_for_ai
        ).model_dump()
        assert response.json() == expected


@pytest.mark.asyncio(loop_scope='session')
async def test_get_minimum_tokens_for_compose_essay():
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get(
            '/ai/minimum-tokens-for-compose-essay/',
        )

        assert response.status_code == 200
        expected = ai_schema.MinimumTokensForComposeEssayResponse(
            tokens=settings.ai.min_tokens_for_essay
        ).model_dump()
        assert response.json() == expected


@pytest.mark.asyncio(loop_scope='session')
async def test_request_ai(access_token):
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        request_data = {
            "text": "Hi",
            "model": "gpt-4o-mini"
        }
        response = await ac.post(
            '/ai/ask/',
            json=request_data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 200


@pytest.mark.asyncio(loop_scope='session')
async def test_compose_essay(access_token):
    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app)
    ) as ac:
        request_data = {
            "theme": "Трагизм Мцыри",
            "author": "Н. Ю. Лермонтов",
            "word_count": 1,  # Program will generate 50 + 1 word
            "additional_info": "Трагический герой"
        }
        response = await ac.post(
            '/ai/compose/essay/',
            json=request_data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 200
