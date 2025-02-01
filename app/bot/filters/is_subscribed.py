# app/bot/filters/is_subscribed.py

import logging
from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from sqlalchemy import text

from app.core.databases.postgres import get_session
from app.bot.models import Channel


class IsSubscribed(BaseFilter):
    """
    Checks whether the user is subscribed to all channels in DB.
    If not, returns False.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user_id = event.from_user.id
        async with get_session() as session:
            channels = await session.execute(text("""SELECT chanel_id FROM channels"""))
            channels_list = channels.scalars().all()

        # If there are no channels to check, pass
        if not channels_list:
            return True

        # Check each channel subscription
        for ch_id in channels_list:
            try:
                member = await self.bot.get_chat_member(chat_id=ch_id, user_id=user_id)
                # member.status can be "creator", "administrator", "member", "restricted", "left", "kicked"
                if member.status in ["left", "kicked"]:
                    return False
            except Exception as e:
                logging.error(f"Failed to fetch chat member: {e}")
                return False
        return True
