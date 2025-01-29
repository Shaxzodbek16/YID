from aiogram.types import Message
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.databases.postgres import get_session
from app.bot.models.channel import Channel


class ChannelRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session = session

    async def create_channel(self, message: Message):
        pass

    async def is_exists(self, channel_id: int) -> bool:
        result = await self.__session.execute(
            select(Channel).where(Channel.channel_id == channel_id)
        )
        return True if result.scalar_one_or_none() else False

    async def get_channel(self, channel_id: int) -> Channel | None:
        result = await self.__session.execute(
            select(Channel).where(Channel.channel_id == channel_id)
        )
        return result.scalar_one_or_none()

    async def get_channels(self) -> list[Channel]:
        result = await self.__session.execute(select(Channel))
        return [channel for channel in result.scalars().all()]

    async def update_channel(
        self, channel_id: int, chanel_name: str, channel_link: str
    ) -> bool:
        existing_channel = await self.get_channel(channel_id)
        if existing_channel:
            setattr(existing_channel, chanel_name, chanel_name)
            setattr(existing_channel, channel_link, channel_link)
            await self.__session.commit()
            await self.__session.refresh(existing_channel)
            return True
        return False

    async def delete_channel(self, channel_id: int):
        channel = await self.get_channel(channel_id)
        if channel:
            await self.__session.delete(channel)
            await self.__session.commit()
            return True
        return False
