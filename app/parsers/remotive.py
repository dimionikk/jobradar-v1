import httpx
from typing import Optional
from bs4 import BeautifulSoup
from datetime import datetime
REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


async def fetch_remotive_vacancies() -> list[dict]:

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(REMOTIVE_API_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError:
            return []

    vacancies = []
    for job in data.get("jobs", []):
        vacancy = _parse_job(job)
        if vacancy:
            vacancies.append(vacancy)

    return vacancies

def _parse_job(job: dict) -> Optional[dict]:
    url = job.get("url")
    title = job.get("title")
    company = job.get("company_name")

    if not url or not title or not company:
        return None

    description = job.get("description", "")
    if description:
        description = BeautifulSoup(description, "lxml").get_text(separator=" ").strip()[:5000]

    created_at = None
    date_str = job.get("publication_date")
    if date_str:
        try:
            created_at = datetime.fromisoformat(date_str)
        except ValueError:
            created_at = None

    return {
        "title": title,
        "company": company,
        "description": description,
        "salary_min": None,
        "salary_max": None,
        "city": None,
        "work_type": "remote",
        "experience": None,
        "url": url,
        "source": "remotive",
        "created_at": created_at,
    }