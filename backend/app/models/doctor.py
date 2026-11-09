
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    Text,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    specialization: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    qualification: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    consultation_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="doctor_profile"
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )

    # A doctor can work at multiple hospitals.
    hospital_assignments = relationship(
        "DoctorHospital",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )
