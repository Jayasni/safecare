from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.availability_slot import AvailabilitySlot
from app.models.booking import Booking, BookingStatus


class AvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, slot_id: int) -> AvailabilitySlot | None:
        return self.db.get(AvailabilitySlot, slot_id)

    def get_by_id_for_update(self, slot_id: int) -> AvailabilitySlot | None:
        return (
            self.db.query(AvailabilitySlot)
            .filter(AvailabilitySlot.id == slot_id)
            .with_for_update()
            .first()
        )

    def list(
        self,
        *,
        service_id: int | None = None,
        provider_id: int | None = None,
        active_only: bool = True,
        upcoming_only: bool = False,
    ) -> list[AvailabilitySlot]:
        query = self.db.query(AvailabilitySlot)
        if active_only:
            query = query.filter(AvailabilitySlot.is_active.is_(True))
        if service_id is not None:
            query = query.filter(AvailabilitySlot.service_id == service_id)
        if provider_id is not None:
            query = query.filter(AvailabilitySlot.provider_id == provider_id)
        if upcoming_only:
            query = query.filter(AvailabilitySlot.start_time > datetime.now(datetime.timezone.utc))
        return query.order_by(AvailabilitySlot.start_time).all()

    def has_conflict(
        self,
        *,
        provider_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_slot_id: int | None = None,
    ) -> bool:
        query = self.db.query(AvailabilitySlot).filter(
            AvailabilitySlot.provider_id == provider_id,
            AvailabilitySlot.is_active.is_(True),
            AvailabilitySlot.start_time < end_time,
            AvailabilitySlot.end_time > start_time,
        )
        if exclude_slot_id is not None:
            query = query.filter(AvailabilitySlot.id != exclude_slot_id)
        return query.first() is not None

    def active_booking_count(self, slot_id: int) -> int:
        return (
            self.db.query(func.count(Booking.id))
            .filter(
                Booking.slot_id == slot_id,
                Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
            )
            .scalar()
            or 0
        )

    def create(self, slot: AvailabilitySlot) -> AvailabilitySlot:
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def update(self, slot: AvailabilitySlot) -> AvailabilitySlot:
        self.db.commit()
        self.db.refresh(slot)
        return slot