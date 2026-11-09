
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class MedicalService(Base):
    __tablename__ = "medical_services"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    hospital_id: Mapped[int] = mapped_column(
        ForeignKey("hospitals.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    hospital = relationship(
        "Hospital",
        back_populates="services"
    )

    appointments = relationship(
        "Appointment",
        back_populates="service"
    )

    # Doctors assigned to provide this service.
    doctor_assignments = relationship(
        "DoctorHospitalService",
        back_populates="service"
    )
