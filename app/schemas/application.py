from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ApplicationCreate(BaseModel):
    vacancy_id: int
    note: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    status: str
    note: Optional[str] = None
    applied_at: datetime

    model_config = {"from_attributes": True}