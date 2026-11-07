from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.models.enums import BookingStatus
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingHistoryResponse,
    BookingReschedule,
    BookingResponse,
)
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def require_owner_or_admin(booking, current_user: User):
    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot access this booking")


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)
    try:
        return service.create_booking(current_user.id, payload.slot_id, payload.reason)
    except HTTPException:
        raise


@router.get("/my", response_model=list[BookingResponse])
def list_my_bookings(
    status: BookingStatus | None = Query(default=None),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService(db).list_customer_bookings(
        current_user.id, status, from_date, to_date, offset, limit
    )


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)
    booking = service.get_booking(current_user, booking_id)
    return booking


@router.patch("/{booking_id}/reschedule", response_model=BookingResponse)
def reschedule_booking(
    booking_id: int,
    payload: BookingReschedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService(db).reschedule_booking(
        current_user, booking_id, payload.new_slot_id
    )


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService(db).cancel_booking(current_user, booking_id)


@router.get("/{booking_id}/history", response_model=list[BookingHistoryResponse])
def booking_history(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService(db).get_booking_history(current_user, booking_id)