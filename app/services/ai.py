import httpx
from app.models.user import User
from app.models.vacancy import Vacancy
import json
from app.core.config import settings

def _build_user_profile(user: User) -> str:
    return f"""
Профіль кандидата:
- Стек: {user.stack or 'не вказано'}
- Досвід: {user.experience or 'не вказано'}
- Очікувана зарплата: {user.salary_min or '?'} - {user.salary_max or '?'} USD
- Місто: {user.city or 'не вказано'}
- Тип роботи: {user.work_type or 'не вказано'}
- Про себе: {user.description or 'не вказано'}
""".strip()


def _build_vacancy_info(vacancy: Vacancy) -> str:
    return f"""
Вакансія:
- Назва: {vacancy.title}
- Компанія: {vacancy.company}
- Зарплата: {vacancy.salary_min or '?'} - {vacancy.salary_max or '?'} USD
- Місто: {vacancy.city or 'не вказано'}
- Тип роботи: {vacancy.work_type or 'не вказано'}
- Опис: {vacancy.description or 'не вказано'}
""".strip()


async def analyze_vacancy(user: User, vacancy: Vacancy) -> dict:
    user_profile = _build_user_profile(user)
    vacancy_info = _build_vacancy_info(vacancy)

    prompt = f"""
{user_profile}

{vacancy_info}

Проаналізуй наскільки ця вакансія підходить кандидату.
Відповідай ТІЛЬКИ в такому форматі JSON і нічого більше:
{{
    "match_percent": <число від 0 до 100>,
    "pros": ["<плюс 1>", "<плюс 2>"],
    "cons": ["<мінус 1>", "<мінус 2>"],
    "summary": "<короткий висновок 2-3 речення>"
}}
"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    text = data["content"][0]["text"].strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


async def generate_cover_letter(user: User, vacancy: Vacancy) -> str:
    user_profile = _build_user_profile(user)
    vacancy_info = _build_vacancy_info(vacancy)

    prompt = f"""
{user_profile}

{vacancy_info}

Напиши супровідний лист для цієї вакансії від імені кандидата.
Лист повинен бути професійним, конкретним і не довшим за 200 слів.
"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    return data["content"][0]["text"]