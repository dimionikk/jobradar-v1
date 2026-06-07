from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_authenticated_user
from app.models.user import User
from app.schemas.user import UserResponse, UpdateProfileRequest
from app.services.auth import update_profile, delete_account

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_model=UserResponse)
async def get_profile(
    user: User = Depends(get_authenticated_user)
):
    return user


@router.patch("/", response_model=UserResponse)
async def update_user_profile(
    data: UpdateProfileRequest,
    user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    return await update_profile(user, data, db)


@router.delete("/", status_code=204)
async def delete_user_account(
    user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    await delete_account(user, db)