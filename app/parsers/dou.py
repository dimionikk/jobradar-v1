import httpx
from bs4 import BeautifulSoup
from typing import Optional
import asyncio


CATEGORIES = ["Python", "JavaScript", "Java", "DevOps", "QA", "Design"]

DOU_BASE_URL = "https://jobs.dou.ua/vacancies/?remote&category="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def fetch_dou_vacancies() -> list[dict]:
    all_vacancies = []

    async with httpx.AsyncClient(headers=HEADERS) as client:
        for category in CATEGORIES:
            url = DOU_BASE_URL + category
            try:
                response = await client.get(url, timeout=30)
                response.raise_for_status()
            except httpx.HTTPError:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select("li.l-vacancy")

            for item in items:
                vacancy = await _parse_item(client, item)
                if vacancy:
                    all_vacancies.append(vacancy)

    return all_vacancies


async def _parse_item(client: httpx.AsyncClient, item) -> Optional[dict]:
    title_tag = item.select_one("a.vt")
    company_tag = item.select_one("a.company")

    if not title_tag or not company_tag:
        return None

    url = title_tag.get("href", "")
    title = title_tag.get_text(strip=True)
    company = company_tag.get_text(strip=True)

    description = None
    try:
        response = await client.get(url, timeout=30)
        response.raise_for_status()
        detail_soup = BeautifulSoup(response.text, "lxml")
        desc_tag = detail_soup.select_one("div.b-typo.vacancy-section")
        if desc_tag:
            description = desc_tag.get_text(separator=" ", strip=True).replace("\xa0", " ")[:5000]
    except httpx.HTTPError:
        pass

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
        "source": "dou",
        "created_at": None,
    }