from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_authenticated_user as get_current_user
from app.models.user import User
from app.schemas.vacancy import VacancyResponse, VacancyFilter
from app.services.vacancy import get_vacancies, get_vacancy_by_id

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/", response_model=list[VacancyResponse])
async def list_vacancies(
    filters: VacancyFilter = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vacancies = await get_vacancies(db, filters)
    return vacancies


@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vacancy = await get_vacancy_by_id(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy