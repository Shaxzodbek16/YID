from aiogram.types import Message

from app.bot.handlers.user.get_user import get_user
from app.bot.models import User
from app.core.databases.postgres import get_session


async def create_or_update_user(message: Message):
    async with get_session() as session:
        user = await get_user(message.from_user.id)
        if user is not None:
            user.username = message.from_user.username
            user.first_name = message.from_user.first_name
            user.last_name = message.from_user.last_name
            user.language_code = message.from_user.language_code
            user.is_premium = message.from_user.is_premium
            user.last_login = message.date
        else:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code,
                is_premium=message.from_user.is_premium,
                last_login=message.date,
            )
        session.add(user)
        await session.commit()
        await session.refresh(user)
