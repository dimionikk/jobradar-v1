from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VacancyResponse(BaseModel):
    id: int
    title: str
    company: str
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: Optional[str] = None
    work_type: Optional[str] = None
    experience: Optional[str] = None
    url: str
    source: str
    created_at: Optional[datetime] = None
    parsed_at: datetime


class VacancyFilter(BaseModel):
    source: Optional[str] = None
    work_type: Optional[str] = None
    experience: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: Optional[str] = None