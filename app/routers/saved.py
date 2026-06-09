from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_authenticated_user
from app.models.user import User
from app.schemas.saved_vacancy import SavedVacancyResponse
from app.services.vacancy import save_vacancy, unsave_vacancy, get_saved_vacancies

router = APIRouter(prefix="/saved", tags=["saved"])

@router.get("/", response_model=list[SavedVacancyResponse])
async def list_saved(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    return await get_saved_vacancies(db, current_user.id)

@router.post("/{vacancy_id}", response_model=SavedVacancyResponse, status_code=201)
async def save(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    return await save_vacancy(db, current_user.id, vacancy_id)

@router.delete("/{vacancy_id}", status_code=204)
async def unsave(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    result = await unsave_vacancy(db, current_user.id, vacancy_id)
    if not result:
        raise HTTPException(status_code=404, detail="Saved vacancy not found")