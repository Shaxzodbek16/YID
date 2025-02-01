from aiogram import Router
from aiogram.filters import Command

from app.bot.constants.users import help_message
from app.bot.keyboards.user import user_step_1

router = Router()


@router.message(Command("help"))
async def start(message):
    await message.answer(help_message, reply_markup=await user_step_1())
