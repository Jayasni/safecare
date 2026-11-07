from datetime import datetime

from pydantic import EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import ORMModel


class UserBase(ORMModel):
    full_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(ORMModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=32)


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime