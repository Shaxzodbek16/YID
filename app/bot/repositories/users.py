from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select

from app.bot.models.users import User


class UserRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker

    async def get_user(self, telegram_id: int) -> User | None:
        async with self._session_maker() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
        return result.scalar_one_or_none()

    async def get_users(self) -> list[User]:
        async with self._session_maker() as session:
            result = await session.execute(select(User))
        return [u for u in result.scalars().all()]

    async def create_user(self, message: Message) -> bool:
        if not await self.is_exists(message.from_user.id):
            async with self._session_maker() as session:
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    is_premium=message.from_user.is_premium,
                    language_code=message.from_user.language_code,
                    created_at=message.date,
                    last_login=message.date,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return True
        user = await self.get_user(message.from_user.id)
        user.last_login = message.date
        async with self._session_maker() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return False

    async def is_exists(self, telegram_id: int) -> bool:
        async with self._session_maker() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
        return True if result.scalar_one_or_none() else False

    async def delete_user(self, telegram_id: int) -> bool:
        async with self._session_maker() as session:
            user = await self.get_user(telegram_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
        return False
