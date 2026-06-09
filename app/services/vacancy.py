from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional

from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyFilter
from app.models.saved_vacancy import SavedVacancy



async def get_vacancies(db: AsyncSession, filters: VacancyFilter) -> list[Vacancy]:
    query = select(Vacancy)

    conditions = []

    if filters.source:
        conditions.append(Vacancy.source == filters.source)

    if filters.work_type:
        conditions.append(Vacancy.work_type == filters.work_type)

    if filters.city:
        conditions.append(Vacancy.city.ilike(f"%{filters.city}%"))

    if filters.salary_min:
        conditions.append(Vacancy.salary_min >= filters.salary_min)

    if filters.salary_max:
        conditions.append(Vacancy.salary_max <= filters.salary_max)

    if filters.search:
        conditions.append(
            Vacancy.title.ilike(f"%{filters.search}%") |
            Vacancy.description.ilike(f"%{filters.search}%")
        )

    if conditions:
        query = query.where(and_(*conditions))

    result = await db.execute(query)
    return result.scalars().all()


async def get_vacancy_by_id(db: AsyncSession, vacancy_id: int) -> Optional[Vacancy]:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id))
    return result.scalar_one_or_none()


async def save_vacancy(db: AsyncSession, user_id: int, vacancy_id: int):
    result = await db.execute(
        select(SavedVacancy).where(
            and_(SavedVacancy.user_id == user_id, SavedVacancy.vacancy_id == vacancy_id)
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    saved = SavedVacancy(user_id=user_id, vacancy_id=vacancy_id)
    db.add(saved)
    await db.commit()
    await db.refresh(saved)
    return saved


async def unsave_vacancy(db: AsyncSession, user_id: int, vacancy_id: int) -> bool:
    result = await db.execute(
        select(SavedVacancy).where(
            and_(SavedVacancy.user_id == user_id, SavedVacancy.vacancy_id == vacancy_id)
        )
    )
    saved = result.scalar_one_or_none()
    if not saved:
        return False

    await db.delete(saved)
    await db.commit()
    return True


async def get_saved_vacancies(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(SavedVacancy).where(SavedVacancy.user_id == user_id)
    )
    return result.scalars().all()