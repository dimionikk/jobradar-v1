from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.vacancy import VacancyResponse


class CreateApplicationRequest(BaseModel):
    vacancy_id: int
    note: Optional[str] = None


class UpdateApplicationRequest(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    vacancy: VacancyResponse
    status: str
    note: Optional[str] = None
    applied_at: datetime