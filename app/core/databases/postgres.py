# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import sessionmaker
#
# from app.core.settings.config import get_settings
#
# settings = get_settings()
#
# DATABASE_URL = f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
#
# engine = create_async_engine(f"postgresql+asyncpg://{DATABASE_URL}", echo=False)
#
# async_session_factory = async_sessionmaker(
#     engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )
#
#
# async def get_session():
#     async with async_session_factory() as session:
#         yield session


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.settings.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DATABASE}"
)

engine = create_async_engine("postgresql+asyncpg://" + DATABASE_URL, echo=False)

SessionMaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
