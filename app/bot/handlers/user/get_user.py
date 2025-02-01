# app/bot/handlers/user/get_user.py

from sqlalchemy import select
from app.bot.models import User
from app.core.databases.postgres import get_session


async def get_user(telegram_id: int) -> User | None:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
