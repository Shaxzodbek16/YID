from typing import Sequence, Optional

from app.bot.models import Channel
from app.core.databases.postgres import get_session
from sqlalchemy import select

from typing import Sequence, Optional
from sqlalchemy import select
from app.core.databases.postgres import get_session
from app.bot.models import Channel


async def get_all_channels() -> Sequence[Channel]:
    async with get_session() as session:
        res = await session.execute(select(Channel))
        return res.scalars().all()


async def get_channel_by_id(channel_id: int) -> Optional[Channel]:
    async with get_session() as session:
        res = await session.execute(select(Channel).where(Channel.id == channel_id))
        return res.scalar_one_or_none()


async def delete_channel_by_id(channel_id: int):  # Change type to int
    async with get_session() as session:
        res = await session.execute(select(Channel).where(Channel.id == channel_id))
        channel = res.scalar_one_or_none()
        if channel:
            await session.delete(channel)
            await session.commit()
