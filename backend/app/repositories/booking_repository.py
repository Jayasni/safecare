from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.availability_slot import AvailabilitySlot
from app.models.booking import Booking, BookingStatus
from app.models.booking_history import BookingHistory


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, booking_id: int, for_update: bool = False) -> Booking | None:
        query = (
            self.db.query(Booking)
            .options(selectinload(Booking.slot), selectinload(Booking.history))
            .filter(Booking.id == booking_id)
        )
        if for_update:
            query = query.with_for_update()
        return query.first()

    def list_by_user(
        self,
        user_id: int,
        status: BookingStatus | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[Booking]:
        query = (
            self.db.query(Booking)
            .options(selectinload(Booking.slot))
            .filter(Booking.user_id == user_id)
        )
        if status is not None:
            query = query.filter(Booking.status == status)
        if from_date is not None or to_date is not None:
            query = query.join(Booking.slot)
            if from_date is not None:
                query = query.filter(AvailabilitySlot.start_time >= from_date)
            if to_date is not None:
                query = query.filter(AvailabilitySlot.start_time <= to_date)
        return query.order_by(Booking.created_at.desc()).offset(offset).limit(limit).all()

    def list_all(
        self,
        status: BookingStatus | None = None,
        user_id: int | None = None,
        service_id: int | None = None,
        provider_id: int | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[Booking]:
        from app.models.availability_slot import AvailabilitySlot

        query = (
            self.db.query(Booking)
            .options(selectinload(Booking.slot))
            .join(Booking.slot)
        )
        if status is not None:
            query = query.filter(Booking.status == status)
        if user_id is not None:
            query = query.filter(Booking.user_id == user_id)
        if service_id is not None:
            query = query.filter(AvailabilitySlot.service_id == service_id)
        if provider_id is not None:
            query = query.filter(AvailabilitySlot.provider_id == provider_id)
        if from_date is not None:
            query = query.filter(AvailabilitySlot.start_time >= from_date)
        if to_date is not None:
            query = query.filter(AvailabilitySlot.start_time <= to_date)
        return query.order_by(Booking.created_at.desc()).offset(offset).limit(limit).all()

    def user_has_active_booking_for_slot(self, user_id: int, slot_id: int) -> bool:
        count = (
            self.db.query(func.count(Booking.id))
            .filter(
                Booking.user_id == user_id,
                Booking.slot_id == slot_id,
                Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
            )
            .scalar()
        )
        return bool(count)

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        # Flush to get DB-generated values without final commit.
        self.db.flush()
        return booking

    def update(self, booking: Booking) -> Booking:
        self.db.flush()
        return booking

    def add_history(self, history: BookingHistory) -> None:
        self.db.add(history)

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, booking: Booking) -> None:
        self.db.refresh(booking)