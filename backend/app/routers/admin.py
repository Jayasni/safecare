
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies_auth import require_roles
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.enums import UserRole, AppointmentStatus


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    total_users = db.query(User).count()
    total_doctors = db.query(Doctor).count()
    total_patients = db.query(Patient).count()
    total_appointments = db.query(Appointment).count()

    pending_appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.PENDING
    ).count()

    confirmed_appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.CONFIRMED
    ).count()

    completed_appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.COMPLETED
    ).count()

    cancelled_appointments = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.CANCELLED
    ).count()

    return {
        "message": "Admin dashboard statistics",
        "admin": current_user.full_name,
        "statistics": {
            "total_users": total_users,
            "total_doctors": total_doctors,
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "pending_appointments": pending_appointments,
            "confirmed_appointments": confirmed_appointments,
            "completed_appointments": completed_appointments,
            "cancelled_appointments": cancelled_appointments
        }
    }
