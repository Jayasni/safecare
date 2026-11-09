
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DoctorCreate(BaseModel):
    user_id: int
    specialization: str = Field(min_length=2, max_length=120)
    qualification: str = Field(min_length=2, max_length=150)
    experience_years: int = Field(default=0, ge=0)
    consultation_fee: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    bio: str | None = None
    is_available: bool = True


class DoctorUpdate(BaseModel):
    specialization: str | None = Field(default=None, min_length=2, max_length=120)
    qualification: str | None = Field(default=None, min_length=2, max_length=150)
    experience_years: int | None = Field(default=None, ge=0)
    consultation_fee: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )
    bio: str | None = None
    is_available: bool | None = None


class DoctorResponse(BaseModel):
    id: int
    user_id: int
    specialization: str
    qualification: str
    experience_years: int
    consultation_fee: Decimal
    bio: str | None
    is_available: bool

    model_config = ConfigDict(from_attributes=True)
