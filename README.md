# JobRadar

AI сервіс для пошуку IT вакансій. Моніторить DOU.ua, Djinni.co, 
Work.ua, Remotive.com — AI аналізує профіль юзера і підбирає 
підходящі вакансії з відсотком відповідності.

## Стек
- FastAPI + PostgreSQL + SQLAlchemy + Alembic
- Anthropic API
- APScheduler
- Docker + Nginx + Hetzner

## Функції
- Реєстрація та авторизація (JWT)
- Автоматичний парсинг вакансій кожні 6 годин
- AI підбір вакансій під профіль юзера
- Відсоток відповідності для кожної вакансії
- Генерація cover letter
- Трекер заявок

## Запуск локально
1. Клонуй репозиторій
2. Створи .env з .env.example
3. Запусти docker-compose up -d
4. Запусти uvicorn app.main:app --reload