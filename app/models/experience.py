import uuid
from sqlalchemy import String, Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    role: Mapped[str] = mapped_column(String(150))
    company: Mapped[str] = mapped_column(String(150))
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    period: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    achievements: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON encoded string list
    technologies: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON encoded string list
    order: Mapped[int] = mapped_column(Integer, default=0)
    current: Mapped[bool] = mapped_column(Boolean, default=False)
