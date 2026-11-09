from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "DoctorCreate",
    "DoctorUpdate",
    "DoctorResponse",
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "AppointmentCreate",
    "AppointmentUpdate",
    "AppointmentResponse",
]