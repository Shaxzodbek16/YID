from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable
from app.core.databases.sqlite import get_session
from sqlalchemy import select
from app.bot.models.channels import Channel
from aiogram.exceptions import TelegramForbiddenError


class ChannelCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        if hasattr(event, "message") and event.message:
            user_id = event.message.from_user.id
            chat_id = event.message.chat.id
        elif hasattr(event, "callback_query") and event.callback_query:
            user_id = event.callback_query.from_user.id
            chat_id = event.callback_query.message.chat.id
        else:
            return await handler(event, data)

        async with get_session() as session:
            result = await session.execute(select(Channel))
            all_channels = result.scalars().all()

            not_joined_channels = []
            for ch in all_channels:
                try:
                    member = await self.bot.get_chat_member(ch.channel_id, user_id)
                    if member.status in ["left", "kicked"]:
                        not_joined_channels.append(ch)
                except TelegramForbiddenError:
                    not_joined_channels.append(ch)

        if not_joined_channels:
            text = "You must join the following channels to use this bot:\n\n"
            for ch in not_joined_channels:
                text += f"➤ {ch.channel_id} ({ch.channel_name})\n"
            await event.message.answer(text)
            return

        return await handler(event, data)
