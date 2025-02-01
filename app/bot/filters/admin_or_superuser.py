import logging

from aiogram.filters import BaseFilter
from typing import Union
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from app.core.databases.postgres import get_session
from app.bot.models.users import User


class IsSuperuserOrAdmin(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        async with get_session() as session:
            admins = await session.execute(
                select(User.telegram_id).where(
                    (User.is_superuser == True) | (User.is_admin == True)
                )
            )
            admins = admins.scalars().all()
            user_id = event.from_user.id
        return user_id in admins
