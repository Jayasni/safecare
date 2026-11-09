
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HospitalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    address: str = Field(min_length=5)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    phone: str = Field(min_length=7, max_length=20)
    email: str | None = Field(default=None, max_length=255)


class HospitalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    address: str | None = Field(default=None, min_length=5)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    email: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class HospitalResponse(BaseModel):
    id: int
    name: str
    description: str | None
    address: str
    city: str
    state: str
    postal_code: str | None
    phone: str
    email: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
