
from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import Gender


class PatientCreate(BaseModel):
    user_id: int
    phone: str = Field(min_length=7, max_length=20)
    date_of_birth: date | None = None
    gender: Gender | None = None
    address: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=20)


class PatientUpdate(BaseModel):
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    date_of_birth: date | None = None
    gender: Gender | None = None
    address: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=20)


class PatientResponse(BaseModel):
    id: int
    user_id: int
    phone: str
    date_of_birth: date | None
    gender: Gender | None
    address: str | None
    emergency_contact: str | None

    model_config = ConfigDict(from_attributes=True)
