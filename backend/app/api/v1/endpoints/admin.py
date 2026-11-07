from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.enums import BookingStatus
from app.models.user import User
from app.schemas.booking import BookingResponse
from app.services.admin_service import AdminService
from app.services.booking_service import BookingService

router = APIRouter(prefix="/admin", tags=["Admin Bookings"])


@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return AdminService(db).dashboard_summary()


@router.get("/bookings", response_model=list[BookingResponse])
def admin_list_bookings(
    status: BookingStatus | None = Query(default=None),
    user_id: int | None = Query(default=None),
    service_id: int | None = Query(default=None),
    provider_id: int | None = Query(default=None),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return BookingService(db).admin_list_bookings(
        status, user_id, service_id, provider_id, from_date, to_date, offset, limit
    )


@router.patch("/bookings/{booking_id}/status", response_model=BookingResponse)
def admin_update_booking_status(
    booking_id: int,
    new_status: BookingStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return BookingService(db).admin_update_status(admin, booking_id, new_status)