# app/core/utils/superuser.py

from app.bot.models.users import User
from app.core.databases.postgres import get_session
from sqlalchemy.future import select


async def create_superuser() -> bool:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == 6521856185)
        )
        superuser = result.scalars().first()  # or .one_or_none()
        if superuser:
            return False

        user = User(
            telegram_id=6521856185,
            username="tmshaxzodbek",
            first_name="Shaxzodbek",
            last_name="Muxtorov",
            language_code="uz",
            is_premium=False,
            is_superuser=True,
            is_admin=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return True
