from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base

from src.core.config import settings


engine = create_async_engine(
    settings.database_settings.url,
    echo=settings.database_settings.echo
)
async_session = async_sessionmaker(bind=engine)


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
