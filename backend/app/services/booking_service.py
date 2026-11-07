from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.booking_history import BookingHistory
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.user_repository import UserRepository


ALLOWED_TRANSITIONS = {
    BookingStatus.pending: {BookingStatus.confirmed, BookingStatus.cancelled},
    BookingStatus.confirmed: {BookingStatus.cancelled, BookingStatus.completed},
    BookingStatus.cancelled: set(),
    BookingStatus.completed: set(),
}


class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.bookings = BookingRepository(db)
        self.slots = AvailabilityRepository(db)
        self.services = ServiceRepository(db)
        self.users = UserRepository(db)

    def _ensure_permission(self, booking: Booking, current_user: User):
        if current_user.role != UserRole.admin and booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You cannot access this booking")

    def _validate_transition(self, old: BookingStatus, new: BookingStatus):
        if new not in ALLOWED_TRANSITIONS.get(old, set()):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid booking status transition from {old.value} to {new.value}",
            )

    def _validate_slot_for_booking(self, slot):
        if slot is None:
            raise HTTPException(status_code=404, detail="Availability slot not found")
        if not slot.is_active:
            raise HTTPException(status_code=400, detail="This availability slot is inactive")
        if slot.start_time <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Cannot book a past appointment slot")
        if slot.service is None or not slot.service.is_active:
            raise HTTPException(status_code=400, detail="The selected service is inactive")
        if slot.provider is not None and not slot.provider.is_active:
            raise HTTPException(status_code=400, detail="The selected provider is inactive")

    def create_booking(self, user_id: int, slot_id: int, reason: str | None):
        slot = self.slots.get_by_id_for_update(slot_id)
        self._validate_slot_for_booking(slot)

        active_bookings = self.slots.active_booking_count(slot.id)
        if active_bookings + 1 > slot.capacity:
            raise HTTPException(status_code=409, detail="The selected slot is full")

        if self.bookings.user_has_active_booking_for_slot(user_id, slot.id):
            raise HTTPException(
                status_code=409, detail="You already have an active booking for this slot"
            )

        try:
            booking = Booking(
                user_id=user_id,
                slot_id=slot.id,
                reason=reason,
                status=BookingStatus.pending,
            )
            self.bookings.create(booking)
            self.bookings.add_history(
                BookingHistory(
                    booking_id=booking.id,
                    event_type="booking_created",
                    old_status=None,
                    new_status=BookingStatus.pending,
                    changed_by=user_id,
                    change_reason=reason,
                )
            )
            self.bookings.commit()
            self.bookings.refresh(booking)
            return booking
        except HTTPException:
            self.bookings.rollback()
            raise
        except Exception as exc:
            self.bookings.rollback()
            raise HTTPException(status_code=500, detail="Could not create booking") from exc

    def get_booking(self, current_user: User, booking_id: int):
        booking = self.bookings.get_by_id(booking_id)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        self._ensure_permission(booking, current_user)
        return booking

    def list_customer_bookings(
        self,
        user_id: int,
        status: BookingStatus | None,
        from_date: datetime | None,
        to_date: datetime | None,
        offset: int,
        limit: int,
    ):
        return self.bookings.list_by_user(
            user_id=user_id,
            status=status,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            limit=limit,
        )

    def reschedule_booking(self, current_user: User, booking_id: int, new_slot_id: int):
        booking = self.bookings.get_by_id(booking_id, for_update=True)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        self._ensure_permission(booking, current_user)

        if booking.status not in {BookingStatus.pending, BookingStatus.confirmed}:
            raise HTTPException(status_code=400, detail="This booking cannot be rescheduled")

        old_slot_id = booking.slot_id
        old_status = booking.status

        if booking.slot is not None and booking.slot.start_time <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Past bookings cannot be rescheduled")

        new_slot = self.slots.get_by_id_for_update(new_slot_id)
        self._validate_slot_for_booking(new_slot)

        if new_slot.id == booking.slot_id:
            raise HTTPException(status_code=400, detail="Choose a different appointment slot")

        active_bookings = self.slots.active_booking_count(new_slot.id)
        if active_bookings + 1 > new_slot.capacity:
            raise HTTPException(status_code=409, detail="The new slot is full")

        if self.bookings.user_has_active_booking_for_slot(booking.user_id, new_slot.id):
            raise HTTPException(
                status_code=409, detail="You already have an active booking for this slot"
            )

        try:
            booking.slot_id = new_slot.id
            self.bookings.update(booking)
            self.bookings.add_history(
                BookingHistory(
                    booking_id=booking.id,
                    event_type="booking_rescheduled",
                    old_status=old_status,
                    new_status=booking.status,
                    changed_by=current_user.id,
                    change_reason=f"Rescheduled from slot {old_slot_id} to slot {new_slot.id}",
                )
            )
            self.bookings.commit()
            self.bookings.refresh(booking)
            return booking
        except HTTPException:
            self.bookings.rollback()
            raise
        except Exception as exc:
            self.bookings.rollback()
            raise HTTPException(status_code=500, detail="Could not reschedule booking") from exc

    def cancel_booking(self, current_user: User, booking_id: int):
        booking = self.bookings.get_by_id(booking_id, for_update=True)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        self._ensure_permission(booking, current_user)

        if booking.status not in {BookingStatus.pending, BookingStatus.confirmed}:
            raise HTTPException(status_code=400, detail="This booking cannot be cancelled")

        old_status = booking.status

        try:
            booking.status = BookingStatus.cancelled
            self.bookings.update(booking)
            self.bookings.add_history(
                BookingHistory(
                    booking_id=booking.id,
                    event_type="booking_cancelled",
                    old_status=old_status,
                    new_status=BookingStatus.cancelled,
                    changed_by=current_user.id,
                    change_reason="Cancelled by user",
                )
            )
            self.bookings.commit()
            self.bookings.refresh(booking)
            return booking
        except HTTPException:
            self.bookings.rollback()
            raise
        except Exception as exc:
            self.bookings.rollback()
            raise HTTPException(status_code=500, detail="Could not cancel booking") from exc

    def get_booking_history(self, current_user: User, booking_id: int):
        booking = self.bookings.get_by_id(booking_id)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        self._ensure_permission(booking, current_user)
        return booking.history

    def admin_list_bookings(
        self,
        status: BookingStatus | None,
        user_id: int | None,
        service_id: int | None,
        provider_id: int | None,
        from_date: datetime | None,
        to_date: datetime | None,
        offset: int,
        limit: int,
    ):
        return self.bookings.list_all(
            status=status,
            user_id=user_id,
            service_id=service_id,
            provider_id=provider_id,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            limit=limit,
        )

    def admin_update_status(self, current_user: User, booking_id: int, new_status: BookingStatus):
        booking = self.bookings.get_by_id(booking_id, for_update=True)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        self._validate_transition(booking.status, new_status)
        old_status = booking.status

        try:
            booking.status = new_status
            self.bookings.update(booking)
            self.bookings.add_history(
                BookingHistory(
                    booking_id=booking.id,
                    event_type="status_updated",
                    old_status=old_status,
                    new_status=new_status,
                    changed_by=current_user.id,
                    change_reason=f"Status updated by administrator to {new_status.value}",
                )
            )
            self.bookings.commit()
            self.bookings.refresh(booking)
            return booking
        except HTTPException:
            self.bookings.rollback()
            raise
        except Exception as exc:
            self.bookings.rollback()
            raise HTTPException(status_code=500, detail="Could not update booking status") from exc