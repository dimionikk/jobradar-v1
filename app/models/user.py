from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    # профіль
    name: Mapped[Optional[str]]
    stack: Mapped[Optional[str]] = mapped_column(Text)
    experience: Mapped[Optional[str]]
    salary_min: Mapped[Optional[int]]
    salary_max: Mapped[Optional[int]]
    city: Mapped[Optional[str]]
    work_type: Mapped[Optional[str]]
    description: Mapped[Optional[str]] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )