from pydantic import BaseModel
from datetime import datetime


class SavedVacancyResponse(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    saved_at: datetime

    model_config = {"from_attributes": True}