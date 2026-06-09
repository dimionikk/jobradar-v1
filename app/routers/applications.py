from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_authenticated_user
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.services.application import (
    create_application,
    get_applications,
    get_application_by_id,
    update_application,
    delete_application,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/", response_model=list[ApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    return await get_applications(db, current_user.id)


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    application = await get_application_by_id(db, application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/", response_model=ApplicationResponse, status_code=201)
async def create(
    data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    application = await create_application(db, current_user.id, data)
    if not application:
        raise HTTPException(status_code=400, detail="Application already exists")
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update(
    application_id: int,
    data: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    application = await update_application(db, application_id, current_user.id, data)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.delete("/{application_id}", status_code=204)
async def delete(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    result = await delete_application(db, application_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")