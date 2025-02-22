from fastapi import HTTPException, status


class InvalidTokenError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TokenExpiredError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidTokenTypeError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token type'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
