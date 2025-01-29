from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.controllers.user.users import UserController

router = Router()


@router.message(CommandStart())
async def start(message: Message, controller: UserController = UserController()):
    await message.answer("Hello!")
    await controller.create_user(message)
    await message.answer("You are registered!")
