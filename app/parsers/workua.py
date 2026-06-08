import httpx
from bs4 import BeautifulSoup
from typing import Optional


WORKUA_URL = "https://www.work.ua/jobs-"

CATEGORIES = ["python", "javascript", "java", "devops", "qa", "design"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def fetch_workua_vacancies() -> list[dict]:
    all_vacancies = []

    async with httpx.AsyncClient(headers=HEADERS) as client:
        for category in CATEGORIES:
            url = WORKUA_URL + category + "/"
            try:
                response = await client.get(url, timeout=30)
                response.raise_for_status()
            except httpx.HTTPError:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select("div.card.card-hover.job-link")

            for item in items:
                vacancy = _parse_item(item)
                if vacancy:
                    all_vacancies.append(vacancy)

    return all_vacancies


def _parse_item(item) -> Optional[dict]:
    title_tag = item.select_one("h2 a")
    company_tag = item.select_one("span.strong-600")
    desc_tag = item.select_one("p.ellipsis")

    if not title_tag:
        return None

    url = "https://www.work.ua" + title_tag.get("href", "")
    title = title_tag.get_text(strip=True)
    company = company_tag.get_text(strip=True) if company_tag else "Невідома компанія"
    description = desc_tag.get_text(separator=" ", strip=True).replace("\xa0", " ")[:5000] if desc_tag else None

    return {
        "title": title,
        "company": company,
        "description": description,
        "salary_min": None,
        "salary_max": None,
        "city": None,
        "work_type": None,
        "experience": None,
        "url": url,
        "source": "workua",
        "created_at": None,
    }