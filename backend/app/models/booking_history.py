from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlAlchemyEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import BookingStatus


class BookingHistory(Base):
    __tablename__ = "booking_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    old_status: Mapped[BookingStatus | None] = mapped_column(
        SqlAlchemyEnum(BookingStatus, name="booking_status", native_enum=True, create_type=False),
        nullable=True,
    )
    new_status: Mapped[BookingStatus | None] = mapped_column(
        SqlAlchemyEnum(BookingStatus, name="booking_status", native_enum=True, create_type=False),
        nullable=True,
    )
    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    change_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    booking = relationship("Booking", back_populates="history")
    changed_by_user = relationship("User")