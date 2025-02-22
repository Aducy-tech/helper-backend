from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column()
    tokens_count: Mapped[int] = mapped_column(default=1500)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=True)
