from sqlalchemy.future import select

from app.bot.models import User
from app.core.databases.postgres import get_session


async def is_exist(telegram_id: int) -> bool:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        if result.scalar_one_or_none():
            return False
    return True
