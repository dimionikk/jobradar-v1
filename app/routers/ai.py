from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_authenticated_user
from app.models.user import User
from app.services.ai import analyze_vacancy, generate_cover_letter
from app.services.vacancy import get_vacancy_by_id

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze-vacancy/{vacancy_id}")
async def analyze_vacancy_route(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    vacancy = await get_vacancy_by_id(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    result = await analyze_vacancy(current_user, vacancy)
    return result


@router.post("/cover-letter/{vacancy_id}")
async def cover_letter_route(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    vacancy = await get_vacancy_by_id(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    letter = await generate_cover_letter(current_user, vacancy)
    return {"cover_letter": letter}