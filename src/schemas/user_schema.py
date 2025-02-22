from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(min_length=4, max_length=15, examples=['Kwers'])
    email: EmailStr = Field(examples=['user@example.com'])


class UserCreate(UserBase):
    password: str = Field(examples=['12345'])


class UserToAddInDB(UserBase):
    hashed_password: bytes


class UserCreateResponse(UserBase):
    pass


class UserLogin(UserBase):
    username: str | None = Field(examples=['Kwers'])
    email: str | None = Field(examples=['user@example.com'])
    password: str = Field(examples=['12345'])


class UserTokensResponse(BaseModel):
    tokens_count: int = Field(examples=[100])
