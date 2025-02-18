from sqlalchemy import Column, String, DateTime, func, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(255), nullable=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_superuser = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    downloads = relationship("Downloads", back_populates="user")

    def __repr__(self):
        return f"<User {self.telegram_id}>"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
