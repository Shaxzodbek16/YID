from aiogram.types import Message
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.databases.postgres import get_session
from app.bot.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session = session

    async def create_user(self, message: Message):
        if not await self.is_exists(message.from_user.id):
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            self.__session.add(user)
            await self.__session.commit()
            await self.__session.refresh(user)
        else:
            await message.answer("You are already registered!")

    async def is_exists(self, telegram_id: int) -> bool:
        result = await self.__session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return True if result.scalar_one_or_none() else False
