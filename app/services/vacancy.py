from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional

from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyFilter


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