import src.repositories.user_repository as user_repository

from fastapi import APIRouter, status, Depends

from src.schemas import ai_schema
from src.core.config import settings
from src.utils import auth_utils, response_utils
from src.exceptions import user_exceptions
from src.utils.ai import ai_utils
from src.enums.ai_models import Model


router = APIRouter(
    prefix='/ai',
    tags=['ai']
)


@router.post(
    '/ask/',
    response_model=ai_schema.AIResponse,
    status_code=status.HTTP_200_OK,
    responses={
        **response_utils.combine_error_responses(
            auth_utils.get_auth_responses()
        ),
        status.HTTP_400_BAD_REQUEST: response_utils.get_error_response_schema(
            user_exceptions.UserTokensNotEnoughError.detail
        )
    }
)
async def request_ai(
    request: ai_schema.AIRequest,
    user_payload: dict = Depends(auth_utils.get_token_payload)
):
    await auth_utils.validate_token_type(
        token_type=settings.auth_jwt.access_token_name,
        payload=user_payload
    )

    user_id = int(user_payload['sub'])
    user = await user_repository.get_user(user_id=user_id)

    if user.tokens_count < settings.ai.min_tokens_for_ai:
        raise user_exceptions.UserTokensNotEnoughError()

    ai_response = await ai_utils.ai_request(
        request=request.text,
        model=request.model
    )

    tokens_count = await ai_utils.get_tokens_count(
        text=ai_response,
        model=request.model
    )
    new_user_tokens_count = user.tokens_count - tokens_count
    await user_repository.update_user_tokens_count(
        user_id,
        new_user_tokens_count
    )

    return ai_schema.AIResponse(text=ai_response, tokens=tokens_count)


@router.get(
    '/minimum-tokens-for-ai/',
    response_model=ai_schema.MinimumTokensForAIResponse,
    status_code=status.HTTP_200_OK
)
async def get_minimum_tokens_for_ai():
    return ai_schema.MinimumTokensForAIResponse(
        tokens=settings.ai.min_tokens_for_ai
    )


@router.post(
    '/compose/essay/',
    response_model=ai_schema.ComposeEssayResponse,
    status_code=status.HTTP_200_OK,
    responses={
        **response_utils.combine_error_responses(
            auth_utils.get_auth_responses()
        ),
        status.HTTP_400_BAD_REQUEST: response_utils.get_error_response_schema(
            user_exceptions.UserTokensNotEnoughError.detail
        )
    }
)
async def compose_essay(
    request: ai_schema.ComposeEssayRequest,
    user_payload: dict = Depends(auth_utils.get_token_payload)
):
    await auth_utils.validate_token_type(
        token_type=settings.auth_jwt.access_token_name,
        payload=user_payload
    )
    user_id = int(user_payload['sub'])
    user = await user_repository.get_user(user_id=user_id)

    if user.tokens_count < settings.ai.min_tokens_for_essay:
        raise user_exceptions.UserTokensNotEnoughError()

    request_text = await ai_utils.get_request_for_compose_essay(request)

    ai_response = await ai_utils.ai_request(
        request=request_text,
        model=Model.GPT_4O_MINI,
        system_text=settings.ai.system_text_for_essay
    )

    tokens_count = await ai_utils.get_tokens_count(
        text=ai_response,
        model=Model.GPT_4O_MINI
    )
    new_user_tokens_count = user.tokens_count - tokens_count

    await user_repository.update_user_tokens_count(
        user_id,
        new_user_tokens_count
    )

    return ai_schema.ComposeEssayResponse(
        text=ai_response,
        tokens=tokens_count
    )


@router.get(
    '/minimum-tokens-for-compose-essay/',
    response_model=ai_schema.MinimumTokensForComposeEssayResponse,
    status_code=status.HTTP_200_OK
)
async def get_minimum_tokens_for_compose_essay():
    return ai_schema.MinimumTokensForComposeEssayResponse(
        tokens=settings.ai.min_tokens_for_essay
    )
