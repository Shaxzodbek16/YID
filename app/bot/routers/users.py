from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.bot.controllers.channel import ChannelController
from app.bot.controllers.users import UserController
from app.bot.filters.admin import IsAdmin
from app.bot.keyboards.admin import admin_main_menu
from app.core.settings.config import get_settings, Settings

settings: Settings = get_settings()

router = Router()


@router.message(CommandStart())
async def start(message: Message, controller: UserController = UserController()):
    await message.answer("Hello!")
    await controller.create_user(message)
    await message.answer("You have been successfully registered!")


@router.message(Command("channels"))
async def admin_router(
    message: Message, controller: ChannelController = ChannelController()
):
    if message.from_user.id in settings.admins:
        users = await controller.get_all_channels()
        for user in users:
            await message.answer(f"{user.channel_name} - {user.channel_link}")
    else:
        await message.answer("You are not an admin!")


@router.message(Command("admin"))
async def admin_router(message: Message):
    if message.from_user.id in settings.admins:
        await message.answer("Welcome to the admin panel!")
        await message.answer("Choose an option:", reply_markup=admin_main_menu())

    else:
        await message.answer("You are not an admin!")


@router.message(F.text == "Get all users")
async def admin_stats(message: Message, controller: UserController = UserController()):
    if message.from_user.id in settings.admins:
        users = await controller.get_all_users()
        for user in users:
            await message.answer(
                f"{user.telegram_id} - {user.username} - {user.first_name} - {user.last_name}"
            )
    else:
        await message.answer("You are not an admin!")


@router.message(F.text == "Get all channels" and IsAdmin())
async def admin_stats(
    message: Message, controller: ChannelController = ChannelController()
):
    users = await controller.get_all_channels()
    await message.answer(f"{users.channel_name} - {users.channel_link}")



@router.message(F.text == "Send message")
async def send_message(message: Message):
    if message.from_user.id in settings.admins:
        await message.answer("Enter the message you want to send:")
    else:
        await message.answer("You are not an admin!")


@router.message(F.text)
async def send_message(message: Message, controller: UserController = UserController()):
    if message.from_user.id in settings.admins:
        for user in await controller.get_all_users():
            try:
                await message.bot.send_message(user.telegram_id, message.text)
            except Exception as e:
                print(e)
    else:
        await message.answer("You are not an admin!")
