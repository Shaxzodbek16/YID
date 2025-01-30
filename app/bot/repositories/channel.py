from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select

from app.bot.models.channel import Channel


class ChannelRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker

    async def create_channel(self, chanel_name: str, chanel_link: str) -> bool:
        if await self.is_exists(chanel_link):
            return False
        async with self._session_maker() as session:
            channel = Channel(
                channel_name=chanel_name,
                channel_link=chanel_link,
            )
            session.add(channel)
            await session.commit()
            await session.refresh(channel)
            return True

    async def is_exists(self, chanel_link: str) -> bool:
        async with self._session_maker() as session:
            result = await session.execute(
                select(Channel).where(Channel.channel_link == chanel_link)
            )
        return True if result.scalar_one_or_none() else False

    async def get_channel(self, chanel_link: str) -> Channel | None:
        async with self._session_maker() as session:
            result = await session.execute(
                select(Channel).where(Channel.channel_link == chanel_link)
            )
        return result.scalar_one_or_none()

    async def get_channels(self) -> list[Channel]:
        async with self._session_maker() as session:
            result = await session.execute(select(Channel))
            return [channel for channel in result.scalars().all()]

    async def update_channel(
        self, chanel_link: str, chanel_name: str,
    ) -> bool:
        existing_channel = await self.get_channel(chanel_link)
        if existing_channel:
            async with self._session_maker() as session:
                setattr(existing_channel, chanel_name, chanel_link)
                await session.commit()
                await session.refresh(existing_channel)
                return True
        return False

    async def delete_channel(self, chanel_link: str):
        channel = await self.get_channel(chanel_link)
        if channel:
            async with self._session_maker() as session:
                await session.delete(channel)
                await session.commit()
                return True
        return False
