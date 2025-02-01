import datetime
import os

from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from app.bot.models.users import User
from app.bot.models.downloads import Downloads
from app.core.databases.postgres import get_session


async def _count_new_users_since(since_date: datetime.datetime) -> int:
    async with get_session() as session:
        res = await session.scalar(
            select(func.count(User.id)).where(User.created_at >= since_date)
        )
    return res


async def _get_top_user_by_downloads(is_video: bool) -> str:
    async with get_session() as session:
        result = await session.execute(
            select(Downloads.user_id, func.count(Downloads.id).label("download_count"))
            .where(Downloads.type == "mp4")
            .group_by(Downloads.user_id)
            .order_by(desc("download_count"))
            .limit(5)
        )
        row = result.first()

        if not row:
            return "No data"

        user_id, download_count = row
        user = await session.get(User, user_id)
        if not user:
            return "Unknown user"
        username_part = f"(@{user.username})" if user.username else ""
        return f"{user.first_name} {user.last_name or ''} {username_part} – {download_count} downloads"


async def _get_top_format() -> str:
    async with get_session() as session:
        result = await session.execute(
            select(Downloads.format, func.count(Downloads.id).label("format_count"))
            .group_by(Downloads.format)
            .order_by(desc("format_count"))
            .limit(5)
        )
        row = result.first()

        if not row or not row[0]:
            return "No data"

        top_format, count_ = row
        return f"{top_format} – {count_} downloads"


async def statistics_data() -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    day_ago = now - datetime.timedelta(days=1)
    week_ago = now - datetime.timedelta(days=7)
    month_ago = now - datetime.timedelta(days=30)
    year_ago = now - datetime.timedelta(days=365)

    async with get_session() as session:
        today_count = await _count_new_users_since(day_ago)
        week_count = await _count_new_users_since(week_ago)
        month_count = await _count_new_users_since(month_ago)
        year_count = await _count_new_users_since(year_ago)

        total_count = await session.scalar(select(func.count(User.id)))

        admins_count = await session.scalar(
            select(func.count(User.id)).where(
                (User.is_admin == True) | (User.is_superuser == True)
            )
        )
        most_video_downloader = await _get_top_user_by_downloads(is_video=True)
        most_mp3_downloader = await _get_top_user_by_downloads(is_video=False)

        most_downloaded_format = await _get_top_format()

    stats_message = (
        f"📊 <b>Statistics Overview</b>\n\n"
        f"<b>New Users (Last 24h)</b>: {today_count}\n"
        f"<b>New Users (Last 7 days)</b>: {week_count}\n"
        f"<b>New Users (Last 30 days)</b>: {month_count}\n"
        f"<b>New Users (Last 365 days)</b>: {year_count}\n"
        f"<b>Total Users</b>: {total_count}\n\n"
        f"<b>Admin Count</b>: {admins_count}\n\n"
        f"<b>User with Most Video Downloads</b>:\n   {most_video_downloader}\n"
        f"<b>User with Most MP3 Downloads</b>:\n   {most_mp3_downloader}\n"
        f"<b>Most Downloaded Format</b>: {most_downloaded_format}\n"
    )

    return stats_message
