from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    company: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text)
    salary_min: Mapped[Optional[int]]
    salary_max: Mapped[Optional[int]]
    city: Mapped[Optional[str]]
    work_type: Mapped[Optional[str]]
    experience: Mapped[Optional[str]]
    url: Mapped[str] = mapped_column(unique=True)
    source: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    parsed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )