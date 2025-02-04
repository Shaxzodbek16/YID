from app.bot.models import User, Downloads
from app.core.databases.postgres import get_session


async def create_downloads(
    user_id: int, url: str, type_: str, format_: str | None = None
):
    async with get_session() as session:
        download = Downloads(user_id=user_id, url=url, type=type_, format=format_)
        session.add(download)
        await session.commit()
        await session.refresh(download)
