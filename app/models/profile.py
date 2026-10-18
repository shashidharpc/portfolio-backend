from datetime import datetime, timezone
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default="default")
    full_name: Mapped[str] = mapped_column(String(100), default="Shashidhar P C")
    title: Mapped[str] = mapped_column(String(150), default="Full Stack Software Engineer")
    headline: Mapped[str] = mapped_column(Text)
    bio: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(100), default="Bengaluru, Karnataka, India")
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    available_for_hire: Mapped[bool] = mapped_column(Boolean, default=True)
    social_links: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON encoded links
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
