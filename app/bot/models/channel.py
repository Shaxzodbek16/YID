import uuid

from app.core.models.base import Base
from sqlalchemy import Column, Integer, String


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String(125), index=True)
    channel_link = Column(String(125), index=True)
    uuid4 = Column(String(40), index=True, unique=True, default=uuid.uuid4())

    def __repr__(self):
        return f"<Channel {self.id} {self.channel_name}>"
