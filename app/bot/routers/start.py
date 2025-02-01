from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.constants.users import start_message
from app.bot.constants.admin import admin_message, superuser_message
from app.bot.filters.admin import IsAdmin
from app.bot.filters.superuser import IsSuperUser
from app.bot.handlers.user.create_or_update import create_or_update_user
from app.bot.handlers.user.get_user import get_user
from app.bot.keyboards.admin import admin_menu
from app.bot.keyboards.user import user_step_1

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await create_or_update_user(message)
    current_user = await get_user(message.from_user.id)
    if current_user.is_superuser:
        await message.answer(
            superuser_message, reply_markup=await admin_menu(is_admin=True)
        )
    elif current_user.is_admin:
        await message.answer(
            admin_message, reply_markup=await admin_menu(is_admin=False)
        )
    else:
        await message.answer(start_message, reply_markup=await user_step_1())
