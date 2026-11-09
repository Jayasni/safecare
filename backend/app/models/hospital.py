
from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    doctor_assignments = relationship(
        "DoctorHospital",
        back_populates="hospital",
        cascade="all, delete-orphan"
    )

    services = relationship(
        "MedicalService",
        back_populates="hospital"
    )

    availabilities = relationship(
        "DoctorAvailability",
        back_populates="hospital"
    )

    appointments = relationship(
        "Appointment",
        back_populates="hospital"
    )
