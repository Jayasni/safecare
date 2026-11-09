
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Numeric,
    Boolean,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class DoctorHospital(Base):
    __tablename__ = "doctor_hospitals"

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "hospital_id",
            name="uq_doctor_hospital"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    hospital_id: Mapped[int] = mapped_column(
        ForeignKey("hospitals.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    consultation_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
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

    doctor = relationship(
        "Doctor",
        back_populates="hospital_assignments"
    )

    hospital = relationship(
        "Hospital",
        back_populates="doctor_assignments"
    )

    # Services provided by this doctor at this hospital.
    services = relationship(
        "DoctorHospitalService",
        back_populates="doctor_hospital",
        cascade="all, delete-orphan"
    )
