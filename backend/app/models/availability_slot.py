from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"
    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_availability_slots_capacity_positive"),
        CheckConstraint("end_time > start_time", name="ck_availability_slots_end_after_start"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    provider_id: Mapped[int | None] = mapped_column(
        ForeignKey("providers.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    service = relationship("Service", back_populates="availability_slots")
    provider = relationship("Provider", back_populates="availability_slots")
    bookings = relationship("Booking", back_populates="slot", cascade="all, delete-orphan")