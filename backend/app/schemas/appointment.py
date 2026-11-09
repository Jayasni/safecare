
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AppointmentStatus


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_datetime: datetime
    duration_minutes: int = Field(default=30, gt=0, le=240)
    reason: str = Field(min_length=3)
    notes: str | None = None


class AppointmentUpdate(BaseModel):
    appointment_datetime: datetime | None = None
    duration_minutes: int | None = Field(default=None, gt=0, le=240)
    reason: str | None = Field(default=None, min_length=3)
    notes: str | None = None
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_datetime: datetime
    duration_minutes: int
    reason: str
    notes: str | None
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
