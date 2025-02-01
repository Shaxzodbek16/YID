from app.core.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    Boolean,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class Downloads(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(500), nullable=False)
    type = Column(String(50), nullable=True)  # mp3, mp4, etc.
    format = Column(String(50), nullable=True)  # 720p, 1080p, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="downloads")

    def __repr__(self):
        return f"<Download {self.id}> (user_id={self.user_id}, url={self.url})"
