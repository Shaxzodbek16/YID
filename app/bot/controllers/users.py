from aiogram.types import Message

from app.bot.repositories.users import UserRepository
from app.core.databases.postgres import SessionMaker


class UserController:
    def __init__(self, user_repository: UserRepository = UserRepository(SessionMaker)):
        self.__user_repository = user_repository

    async def create_user(self, message: Message):
        await self.__user_repository.create_user(message)

    async def get_all_users(self):
        return await self.__user_repository.get_users()
