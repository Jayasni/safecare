from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.provider import Provider
from app.models.service import Service


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def dashboard_summary(self) -> dict:
        status_counts = {
            status.value: 0 for status in BookingStatus
        }
        rows = (
            self.db.query(Booking.status, func.count(Booking.id))
            .group_by(Booking.status)
            .all()
        )
        for status, count in rows:
            status_counts[status.value] = count

        total_services = self.db.query(func.count(Service.id)).scalar() or 0
        active_services = (
            self.db.query(func.count(Service.id))
            .filter(Service.is_active.is_(True))
            .scalar()
            or 0
        )
        total_providers = self.db.query(func.count(Provider.id)).scalar() or 0
        active_providers = (
            self.db.query(func.count(Provider.id))
            .filter(Provider.is_active.is_(True))
            .scalar()
            or 0
        )

        return {
            "total_bookings": sum(status_counts.values()),
            "status_counts": status_counts,
            "total_services": total_services,
            "active_services": active_services,
            "total_providers": total_providers,
            "active_providers": active_providers,
        }