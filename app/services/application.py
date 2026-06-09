from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional

from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

async def create_application(db: AsyncSession, user_id: int, data: ApplicationCreate):
    existing = await db.execute(
        select(Application).where(
            and_(Application.user_id == user_id, Application.vacancy_id == data.vacancy_id)
        )
    )
    if existing.scalar_one_or_none():
        return None

    application = Application(
        user_id=user_id,
        vacancy_id=data.vacancy_id,
        note=data.note,
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application

async def get_applications(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Application).where(Application.user_id == user_id)
    )
    return result.scalars().all()

async def get_application_by_id(db: AsyncSession, application_id: int, user_id: int):
    result = await db.execute(
        select(Application).where(
            and_(Application.id == application_id, Application.user_id == user_id)
        )
    )
    return result.scalar_one_or_none()

async def update_application(db: AsyncSession, application_id: int, user_id: int, data: ApplicationUpdate):
    application = await get_application_by_id(db, application_id, user_id)
    if not application:
        return None

    if data.status is not None:
        application.status = data.status
    if data.note is not None:
        application.note = data.note

    await db.commit()
    await db.refresh(application)
    return application


async def delete_application(db: AsyncSession, application_id: int, user_id: int) -> bool:
    application = await get_application_by_id(db, application_id, user_id)
    if not application:
        return False

    await db.delete(application)
    await db.commit()
    return True