import httpx
from bs4 import BeautifulSoup
from typing import Optional


DJINNI_URL = "https://djinni.co/jobs/?primary_keyword="

CATEGORIES = ["Python", "JavaScript", "Java", "DevOps", "QA", "Design"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def fetch_djinni_vacancies() -> list[dict]:
    all_vacancies = []

    async with httpx.AsyncClient(headers=HEADERS) as client:
        for category in CATEGORIES:
            url = DJINNI_URL + category
            try:
                response = await client.get(url, timeout=30)
                response.raise_for_status()
            except httpx.HTTPError:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select("li.list-jobs__item")

            for item in items:
                vacancy = _parse_item(item)
                if vacancy:
                    all_vacancies.append(vacancy)

    return all_vacancies

def _parse_salary(salary_text: str) -> tuple[Optional[int], Optional[int]]:
    if not salary_text:
        return None, None
    
    import re
    numbers = re.findall(r'\d+', salary_text.replace(" ", ""))
    
    if len(numbers) == 2:
        return int(numbers[0]), int(numbers[1])
    elif len(numbers) == 1:
        return int(numbers[0]), None
    
    return None, None

def _parse_item(item) -> Optional[dict]:
    title_tag = item.select_one("a.job-item__title-link")
    company_tag = item.select_one("a.job-item__company")
    salary_tag = item.select_one("span.public-salary-item")
    desc_tag = item.select_one("div.job-item__description")

    if not title_tag or not company_tag:
        return None

    url = "https://djinni.co" + title_tag.get("href", "")
    title = title_tag.get_text(strip=True)
    company = company_tag.get_text(strip=True)
    description = desc_tag.get_text(separator=" ", strip=True).replace("\xa0", " ")[:5000] if desc_tag else None
    salary_text = salary_tag.get_text(strip=True) if salary_tag else ""
    salary_min, salary_max = _parse_salary(salary_text)
    return {
        "title": title,
        "company": company,
        "description": description,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "city": None,
        "work_type": None,
        "experience": None,
        "url": url,
        "source": "djinni",
        "created_at": None,
    }