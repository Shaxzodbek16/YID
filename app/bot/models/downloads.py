from app.core.models.base import Base
from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

class Downloads(Base):
    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(Text, index=True)
    video_type = Column(String, index=True)