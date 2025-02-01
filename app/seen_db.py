import asyncio
import random
from faker import Faker
from sqlalchemy import select

from app.bot.models.users import User
from app.bot.models.channel import Channel
from app.bot.models.downloads import Downloads
from app.bot.utils.enums import VideoType
from app.core.databases.postgres import get_session

fake = Faker()


async def seed_db():
    """
    Seeds the PostgreSQL database with mock data for testing/development.
    Creates 100 entries for each of User, Channel, and Downloads.
    """

    async with get_session() as session:
        # 1. Generate 100 Users
        for _ in range(1000):
            user = User(
                telegram_id=fake.random_number(digits=10, fix_len=False),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                language_code=fake.language_code(),
                is_premium=random.choice([True, False]),
                created_at=fake.date_time_between(start_date="-2y", end_date="now"),
                last_login=fake.date_time_between(start_date="-2y", end_date="now"),
                is_superuser=False,
                is_admin=False,
            )
            session.add(user)

        # Commit so user IDs are generated
        await session.commit()

        # Retrieve user IDs to reference in Downloads
        user_ids = (await session.scalars(select(User.id))).all()

        # 2. Generate 100 Channels
        for _ in range(1000):
            channel = Channel(
                channel_name=fake.company(),
                channel_link=f"https://t.me/{fake.user_name()}",  # or any link you like
            )
            session.add(channel)

        await session.commit()

        # 3. Generate 100 Downloads
        # Assuming your VideoType has some enum values. Adjust as necessary.
        video_types = list(VideoType)
        formats = ["144p", "240p", "360p", "480p", "720p", "1080p", "MP3"]

        for _ in range(1000):
            download = Downloads(
                url=fake.url(),
                type=random.choice(
                    video_types
                ),  # e.g. VideoType.MP3, VideoType.MP4, etc.
                is_video=random.choice([True, False]),
                format=random.choice(formats),
                user_id=random.choice(user_ids),
            )
            session.add(download)

        await session.commit()

    print("✅ 100 mock rows have been inserted into each table!")
    print("🚀 You can now run your FastAPI app and test the endpoints.")


async def main():
    for i in range(100):
        await asyncio.sleep(0.2)
        await seed_db()
        print(f"✅ 100 mock rows have been inserted into each table! {i+1}")


if __name__ == "__main__":
    asyncio.run(main())
