from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SqlAlchemyEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import BookingStatus


def generate_booking_reference() -> str:
    return f"BK-{uuid4().hex[:12].upper()}"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    booking_reference: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, index=True, default=generate_booking_reference
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    slot_id: Mapped[int] = mapped_column(
        ForeignKey("availability_slots.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[BookingStatus] = mapped_column(
        SqlAlchemyEnum(BookingStatus, name="booking_status", native_enum=True),
        nullable=False,
        default=BookingStatus.pending,
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="bookings")
    slot = relationship("AvailabilitySlot", back_populates="bookings")
    history = relationship(
        "BookingHistory",
        back_populates="booking",
        cascade="all, delete-orphan",
        order_by="BookingHistory.changed_at",
    )