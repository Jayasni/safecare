
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    Text,
    ForeignKey,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.enums import AppointmentStatus


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Hospital where the appointment takes place.
    hospital_id: Mapped[int] = mapped_column(
        ForeignKey("hospitals.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Medical service selected by the patient.
    service_id: Mapped[int] = mapped_column(
        ForeignKey("medical_services.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    appointment_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        SQLAlchemyEnum(
            AppointmentStatus,
            name="appointment_status",
            values_callable=lambda enum: [item.value for item in enum],
            native_enum=False
        ),
        default=AppointmentStatus.PENDING,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )

    hospital = relationship(
        "Hospital",
        back_populates="appointments"
    )

    service = relationship(
        "MedicalService",
        back_populates="appointments"
    )
