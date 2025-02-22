import httpx
import tiktoken

from openai import AsyncOpenAI

from src.schemas import ai_schema
from src.enums.ai_models import Model
from src.core.config import settings


http_client = httpx.AsyncClient(
    proxy=settings.ai.proxy,
    transport=httpx.HTTPTransport(
        local_address='0.0.0.0'
    )
)

client = AsyncOpenAI(
    api_key=settings.ai.openai_api_key,
    http_client=http_client
)


async def ai_request(
    request: str, model: Model,
    system_text: str | None = None
) -> str:
    messages_list = []

    if system_text:
        messages_list.append({"role": "system", "content": system_text})
    messages_list.append({"role": 'user', "content": request})

    chat_completion = await client.chat.completions.create(
        messages=messages_list,
        model=model.value,
        max_tokens=1000
    )
    return chat_completion.choices[0].message.content


async def get_request_for_compose_essay(
    request: ai_schema.ComposeEssayRequest
) -> str:
    text = f"""
    Напиши сочинение на тему: {request.theme}
    Автор: {request.author}
    Количество РУССКИХ слов: {request.word_count + 50}
    Дополнительная информация: {request.additional_info}

    Используй только русский язык.
    """
    return text


async def get_tokens_count(text: str, model: Model) -> int:
    result = 0

    if model == Model.GPT_4O_MINI:
        encoding = tiktoken.encoding_for_model(model.value)
        result = len(encoding.encode(text))

    return result
