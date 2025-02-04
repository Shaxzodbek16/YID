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
    async with get_session() as session:
        for _ in range(100_000):
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
            await session.commit()

        user_ids = (await session.scalars(select(User.telegram_id))).all()
        print("Users created successfully!")

        # 2. Generate 100 Channels
        for _ in range(10):
            channel = Channel(
                channel_name=fake.company(),
                channel_link=f"https://t.me/{fake.user_name()}",
                uuid4=fake.uuid4(),
            )
            session.add(channel)

        await session.commit()
        print("Channels created successfully!")
        video_types = [VideoType.INSTAGRAM.value, VideoType.YOUTUBE.value]
        formats = ["144p", "240p", "360p", "480p", "720p", "1080p", "MP3"]

        for _ in range(10_000):
            download = Downloads(
                url=fake.url(),
                type=random.choice(video_types),
                format=random.choice(formats),
                user_id=random.choice(user_ids),
            )
            session.add(download)

        await session.commit()
        print("Downloads created successfully!")
        await session.close()


if __name__ == "__main__":
    asyncio.run(seed_db())
    print("Database seeded successfully!")
