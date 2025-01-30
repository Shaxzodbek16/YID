from app.bot.repositories.channel import ChannelRepository
from app.core.databases.postgres import SessionMaker


class ChannelController:
    def __init__(
            self, user_repository: ChannelRepository = ChannelRepository(SessionMaker)
    ): 
        self.__user_repository = user_repository

    async def get_all_channels(self):
        return await self.__user_repository.get_channels()

    async def get_channel(self, chanel_link: str):
        return await self.__user_repository.get_channel(chanel_link)

    async def delete_channel(self, chanel_link: str):
        return await self.__user_repository.delete_channel(chanel_link)

    async def update_channel(self, chanel_link: str, new_link: str):
        return await self.__user_repository.update_channel(chanel_link, new_link)

    async def create_channel(self, chanel_link: str):
        return await self.__user_repository.create_channel(chanel_link, chanel_link)

    async def is_exist(self, chanel_link: str):
        return await self.__user_repository.is_exists(chanel_link)
