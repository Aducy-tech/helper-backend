from pydantic import BaseModel
from typing import ClassVar
from fastapi import status


class AccessTokenResponse(BaseModel):
    access_token: str


class RefreshTokenResponse(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    type: str
    sub: str
    iat: int
    exp: int


class InvalidTokenTypeError(BaseModel):
    STATUS_CODE: ClassVar[int] = status.HTTP_401_UNAUTHORIZED
    MESSAGE: ClassVar[str] = 'Invalid token type.'

    status_code: int = STATUS_CODE
    message: str = MESSAGE
