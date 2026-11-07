from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.common import ORMModel


class ServiceBase(ORMModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    duration_minutes: int = Field(gt=0)
    price: Decimal = Field(ge=0)
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ORMModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime