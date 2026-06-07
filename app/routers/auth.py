from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.database import get_db
from app.core.redis import get_redis
from app.schemas.user import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from app.services.auth import register, login, logout, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=UserResponse)
async def register_user(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    return await register(data, db)


@router.post("/login", response_model=TokenResponse)
async def login_user(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await login(data, db)


@router.post("/logout")
async def logout_user(
    authorization: str = Header(...),
    redis: Redis = Depends(get_redis)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    token = authorization.split(" ")[1]
    await logout(token, redis)
    return {"message": "Successfully logged out"}