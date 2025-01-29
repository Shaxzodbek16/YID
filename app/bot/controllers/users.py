from aiogram.types import Message

from app.bot.repositories.users.users import UserRepository


class UserController:
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.__user_repository = user_repository

    async def create_user(self, message: Message):
        await self.__user_repository.create_user(message)
