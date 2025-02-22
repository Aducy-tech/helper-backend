import jwt
import bcrypt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, UTC


from src.core.config import settings
from src.schemas import token_schema
from src.exceptions import token_exceptions, user_exceptions


http_bearer = HTTPBearer(auto_error=False)


async def validate_token_type(
    token_type: str,
    payload: dict
) -> bool | token_schema.InvalidTokenTypeError:
    if payload.get('type') != token_type:
        raise token_exceptions.InvalidTokenTypeError()
    return True


async def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    if not credentials:
        raise user_exceptions.UserNotAuthenticatedError()

    jwt_token = credentials.credentials

    try:
        payload = decode_jwt(token=jwt_token)
    except jwt.DecodeError:
        raise token_exceptions.InvalidTokenError()
    except jwt.ExpiredSignatureError:
        raise token_exceptions.TokenExpiredError()

    return payload


def get_auth_responses() -> dict[int, HTTPException]:
    """Возвращает стандартный набор ответов для аутентификации"""
    return {
        401: [
            user_exceptions.UserNotAuthenticatedError,
            token_exceptions.InvalidTokenError,
            token_exceptions.TokenExpiredError,
            token_exceptions.InvalidTokenTypeError
        ]
    }


def encode_jwt(
    payload: dict,
    expire_minutes: str,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()

    now_time = datetime.now(UTC)
    if expire_timedelta:
        expire = now_time + expire_timedelta
    else:
        expire = now_time + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat=now_time,
        exp=expire,
    )

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded_jwt


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
) -> dict:
    decoded_jwt = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=algorithm
    )
    return decoded_jwt


def hash_password(
    password: str
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )
