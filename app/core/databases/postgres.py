from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.settings.config import get_settings

settings = get_settings()
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.get_postgres_url}", echo=False
)
async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, future=True, autocommit=False
)


@asynccontextmanager
async def get_session():
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
