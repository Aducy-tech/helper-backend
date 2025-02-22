from sqlalchemy import select

from src.database.database import async_session
from src.database.models import User
from src.schemas import user_schema
from src.exceptions import user_exceptions


async def create_user(
    user_to_add: user_schema.UserToAddInDB
) -> user_schema.UserCreateResponse:
    async with async_session() as session:
        user_exists = await session.scalar(
            select(User).where(
                (User.email == user_to_add.email) |
                (User.username == user_to_add.username)
            )
        )

        if user_exists:
            raise user_exceptions.UserAlreadyExistsError()

        session.add(User(**user_to_add.model_dump()))

        await session.commit()
        return user_schema.UserCreateResponse.model_validate(user_to_add)


async def get_user(
    user_id: int | None = None,
    email: str | None = None, username: str | None = None
) -> User | None:
    async with async_session() as session:
        if user_id:
            user = await session.scalar(
                select(User).where(User.id == user_id)
            )
        elif email:
            user = await session.scalar(
                select(User).where(User.email == email)
            )
        elif username:
            user = await session.scalar(
                select(User).where(User.username == username)
            )

        if not user:
            raise user_exceptions.UserNotFoundError()

        return user


async def update_user_tokens_count(user_id: int, tokens_count: int) -> None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.id == user_id)
        )
        user.tokens_count = tokens_count
        await session.commit()
