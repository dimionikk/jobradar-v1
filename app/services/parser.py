from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.vacancy import Vacancy
from app.parsers.remotive import fetch_remotive_vacancies
from app.parsers.dou import fetch_dou_vacancies
from app.parsers.workua import fetch_workua_vacancies


async def run_all_parsers(db: AsyncSession) -> dict:
    results = {
        "remotive": 0,
        "dou": 0,
        "workua": 0,
        "total_new": 0,
    }

    parsers = [
        ("remotive", fetch_remotive_vacancies),
        ("dou", fetch_dou_vacancies),
        ("workua", fetch_workua_vacancies),
    ]

    for source, parser in parsers:
        try:
            vacancies = await parser()
            new_count = await save_vacancies(vacancies, db)
            results[source] = new_count
            results["total_new"] += new_count
        except Exception as e:
            print(f"Parser {source} failed: {e}")

    return results


async def save_vacancies(vacancies: list[dict], db: AsyncSession) -> int:
    new_count = 0

    for vacancy_data in vacancies:
        url = vacancy_data.get("url")
        if not url:
            continue

        result = await db.execute(select(Vacancy).where(Vacancy.url == url))
        existing = result.scalar_one_or_none()

        if existing:
            continue

        vacancy = Vacancy(**vacancy_data)
        db.add(vacancy)
        new_count += 1

    await db.commit()
    return new_count