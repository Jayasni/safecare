from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class AvailabilitySlotBase(ORMModel):
    service_id: int
    provider_id: int | None = None
    start_time: datetime
    end_time: datetime
    capacity: int = Field(gt=0)
    is_active: bool = True


class AvailabilitySlotCreate(AvailabilitySlotBase):
    pass


class AvailabilitySlotUpdate(ORMModel):
    service_id: int | None = None
    provider_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    capacity: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class AvailabilitySlotResponse(AvailabilitySlotBase):
    id: int
    created_at: datetime
    updated_at: datetime