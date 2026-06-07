from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    stack: Optional[str] = None
    experience: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: Optional[str] = None
    work_type: Optional[str] = None
    description: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    stack: Optional[str] = None
    experience: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: Optional[str] = None
    work_type: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"