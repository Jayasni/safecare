from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class ProviderBase(ORMModel):
    full_name: str = Field(min_length=1, max_length=100)
    specialization: str | None = Field(default=None, max_length=100)
    bio: str | None = None
    is_active: bool = True


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(ORMModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    specialization: str | None = Field(default=None, max_length=100)
    bio: str | None = None
    is_active: bool | None = None


class ProviderResponse(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime