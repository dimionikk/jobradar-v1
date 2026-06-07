from pydantic import BaseModel
from datetime import datetime

from app.schemas.vacancy import VacancyResponse


class SavedVacancyResponse(BaseModel):
    id: int
    vacancy: VacancyResponse
    saved_at: datetime