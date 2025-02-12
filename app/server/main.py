import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.core.settings.config import get_settings
from app.core.utils.superuser import create_superuser

from app.bot.routers.start import router as start_router
from app.bot.routers.help import router as help_router
from app.bot.routers.admin import router as admin_router
from app.bot.routers.user.instagram import router as instagram_router
from app.bot.routers.user.youtube import router as youtube_router

settings = get_settings()


async def main():

    os.makedirs("../../media/videos", exist_ok=True)
    os.makedirs("../../media/mp3", exist_ok=True)
    os.makedirs("../../media/docs", exist_ok=True)
    os.makedirs("../../media/gifs", exist_ok=True)
    await create_superuser()
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(help_router)
    dp.include_router(instagram_router)
    dp.include_router(youtube_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
