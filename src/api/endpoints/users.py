from fastapi import APIRouter, status, Depends

from src.utils import auth_utils
from src.repositories import user_repository as crud
from src.schemas import user_schema, token_schema
from src.exceptions import user_exceptions, token_exceptions
from src.core.config import settings
from src.utils.response_utils import (
    get_error_response_schema,
    combine_error_responses
)


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post(
    '/register/',
    response_model=user_schema.UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        user_exceptions.UserAlreadyExistsError.status_code: (
            get_error_response_schema(
                user_exceptions.UserAlreadyExistsError.detail
            )
        )
    },
    description="Register a new user."
)
async def register_user(user_in: user_schema.UserCreate):
    hashed_password = auth_utils.hash_password(user_in.password)

    user_to_add_in_db = user_schema.UserToAddInDB(
        **user_in.model_dump(exclude={'password'}),
        hashed_password=hashed_password
    )

    try:
        response = await crud.create_user(user_to_add=user_to_add_in_db)
    except user_exceptions.UserAlreadyExistsError:
        raise user_exceptions.UserAlreadyExistsError()

    return user_schema.UserCreateResponse.model_validate(response)


@router.post(
    '/login/',
    response_model=token_schema.TokenResponse,
    responses={
        user_exceptions.UserNotEnoughDataError.status_code: (
            get_error_response_schema(
                user_exceptions.UserNotEnoughDataError.detail
            )
        ),
        user_exceptions.UserInvalidCredentialsError.status_code: (
            get_error_response_schema(
                user_exceptions.UserInvalidCredentialsError.detail
            )
        )
    },
    description="Login a user."
)
async def login_user(user_in: user_schema.UserLogin):
    if not user_in.email and not user_in.username:
        raise user_exceptions.UserNotEnoughDataError()
    elif user_in.email:
        user = await crud.get_user(email=user_in.email)
    elif user_in.username:
        user = await crud.get_user(username=user_in.username)

    if not user or not auth_utils.validate_password(
        password=user_in.password,
        hashed_password=user.hashed_password
    ):
        raise user_exceptions.UserInvalidCredentialsError()
    else:
        access_token = auth_utils.encode_jwt(
            payload={
                'type': settings.auth_jwt.access_token_name,
                'sub': str(user.id)
            },
            expire_minutes=settings.auth_jwt.access_token_expire_minutes
        )

        refresh_token = auth_utils.encode_jwt(
            payload={
                'type': settings.auth_jwt.refresh_token_name,
                'sub': str(user.id)
            },
            expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
        )

        return token_schema.TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )


@router.post(
    '/refresh/',
    response_model=token_schema.AccessTokenResponse,
    responses=combine_error_responses({
        status.HTTP_401_UNAUTHORIZED: [
            user_exceptions.UserNotAuthenticatedError,
            token_exceptions.InvalidTokenError,
            token_exceptions.TokenExpiredError,
            token_exceptions.InvalidTokenTypeError
        ],
    }),
    description=(
        "Refresh access token by refresh token and "
        "return new access token."
    )
)
async def refresh_access_token(
    payload: dict = Depends(auth_utils.get_token_payload)
):
    try:
        await auth_utils.validate_token_type(
            token_type=settings.auth_jwt.refresh_token_name,
            payload=payload
        )
    except user_exceptions.UserNotAuthenticatedError:
        raise user_exceptions.UserNotAuthenticatedError()
    except token_exceptions.InvalidTokenTypeError:
        raise token_exceptions.InvalidTokenTypeError()
    except token_exceptions.InvalidTokenError:
        raise token_exceptions.InvalidTokenError()
    except token_exceptions.TokenExpiredError:
        raise token_exceptions.TokenExpiredError()

    access_token = auth_utils.encode_jwt(
        payload={
            'type': settings.auth_jwt.access_token_name,
            'sub': payload.get('sub')
        },
        expire_minutes=settings.auth_jwt.access_token_expire_minutes
    )
    return token_schema.AccessTokenResponse(access_token=access_token)


@router.get(
    '/me/tokens/',
    response_model=user_schema.UserTokensResponse,
    status_code=status.HTTP_200_OK,
    responses=combine_error_responses({
        status.HTTP_401_UNAUTHORIZED: [
            user_exceptions.UserNotAuthenticatedError,
            token_exceptions.InvalidTokenError,
            token_exceptions.TokenExpiredError,
            token_exceptions.InvalidTokenTypeError
        ],
    }),
    description="Get user's tokens count."
)
async def get_user_tokens(
    payload: dict = Depends(auth_utils.get_token_payload)
):
    try:
        await auth_utils.validate_token_type(
            token_type=settings.auth_jwt.access_token_name,
            payload=payload
        )
    except user_exceptions.UserNotAuthenticatedError:
        raise user_exceptions.UserNotAuthenticatedError()
    except token_exceptions.InvalidTokenTypeError:
        raise token_exceptions.InvalidTokenTypeError()
    except token_exceptions.InvalidTokenError:
        raise token_exceptions.InvalidTokenError()
    except token_exceptions.TokenExpiredError:
        raise token_exceptions.TokenExpiredError()

    user_id = int(payload.get('sub'))
    user = await crud.get_user(user_id=user_id)

    return user_schema.UserTokensResponse(tokens_count=user.tokens_count)


@router.get(
    '/me/can_compose_essay/',
    response_model=bool,
    status_code=status.HTTP_200_OK,
    responses=combine_error_responses({
        status.HTTP_401_UNAUTHORIZED: [
            user_exceptions.UserNotAuthenticatedError,
            token_exceptions.InvalidTokenError,
            token_exceptions.TokenExpiredError,
            token_exceptions.InvalidTokenTypeError
        ],
    }),
    description="Check if user can compose essay."
)
async def can_compose_essay(
    payload: dict = Depends(auth_utils.get_token_payload)
):
    try:
        await auth_utils.validate_token_type(
            token_type=settings.auth_jwt.access_token_name,
            payload=payload
        )
    except user_exceptions.UserNotAuthenticatedError:
        raise user_exceptions.UserNotAuthenticatedError()
    except token_exceptions.InvalidTokenTypeError:
        raise token_exceptions.InvalidTokenTypeError()
    except token_exceptions.InvalidTokenError:
        raise token_exceptions.InvalidTokenError()
    except token_exceptions.TokenExpiredError:
        raise token_exceptions.TokenExpiredError()

    user_id = int(payload.get('sub'))
    user = await crud.get_user(user_id=user_id)

    return user.tokens_count >= settings.ai.min_tokens_for_essay


@router.get(
    '/me/can_request_chatgpt/',
    response_model=bool,
    status_code=status.HTTP_200_OK,
    responses=combine_error_responses({
        status.HTTP_401_UNAUTHORIZED: [
            user_exceptions.UserNotAuthenticatedError,
            token_exceptions.InvalidTokenError,
            token_exceptions.TokenExpiredError,
            token_exceptions.InvalidTokenTypeError
        ],
    }),
    description="Check if user can request chatgpt."
)
async def can_request_chatgpt(
    payload: dict = Depends(auth_utils.get_token_payload)
):
    try:
        await auth_utils.validate_token_type(
            token_type=settings.auth_jwt.access_token_name,
            payload=payload
        )
    except user_exceptions.UserNotAuthenticatedError:
        raise user_exceptions.UserNotAuthenticatedError()
    except token_exceptions.InvalidTokenTypeError:
        raise token_exceptions.InvalidTokenTypeError()
    except token_exceptions.InvalidTokenError:
        raise token_exceptions.InvalidTokenError()
    except token_exceptions.TokenExpiredError:
        raise token_exceptions.TokenExpiredError()

    user_id = int(payload.get('sub'))
    user = await crud.get_user(user_id=user_id)

    return user.tokens_count >= settings.ai.min_tokens_for_ai
