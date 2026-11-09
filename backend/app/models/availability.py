
from datetime import datetime, time

from sqlalchemy import (
    ForeignKey,
    Integer,
    Time,
    Boolean,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class DoctorAvailability(Base):
    __tablename__ = "doctor_availability"

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "hospital_id",
            "day_of_week",
            name="uq_doctor_hospital_day"
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

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    slot_duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
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

    doctor = relationship("Doctor")

    hospital = relationship(
        "Hospital",
        back_populates="availabilities"
    )
