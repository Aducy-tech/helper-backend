from fastapi import HTTPException, status


class UserNotAuthenticatedError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User not authenticated'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User already exists'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotEnoughDataError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User not enough data'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserInvalidCredentialsError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid credentials'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserTokensNotEnoughError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User tokens not enough'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
