from datetime import datetime

from pydantic import Field

from app.models.enums import BookingStatus
from app.schemas.common import ORMModel


class BookingCreate(ORMModel):
    slot_id: int
    reason: str | None = None


class BookingReschedule(ORMModel):
    new_slot_id: int


class BookingResponse(ORMModel):
    id: int
    booking_reference: str
    user_id: int
    slot_id: int
    status: BookingStatus
    reason: str | None = None
    created_at: datetime
    updated_at: datetime


class BookingHistoryResponse(ORMModel):
    id: int
    booking_id: int
    event_type: str
    old_status: BookingStatus | None = None
    new_status: BookingStatus | None = None
    changed_by: int | None = None
    change_reason: str | None = None
    changed_at: datetime