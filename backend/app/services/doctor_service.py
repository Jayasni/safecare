
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.enums import UserRole
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.repositories import doctor_repository


def create_doctor(db: Session, doctor_data: DoctorCreate):
    # Check whether the user exists
    user = doctor_repository.get_user_by_id(
        db, doctor_data.user_id
    )

    if user is None:
        raise ValueError("User not found")

    # Only users with doctor role can have a doctor profile
    if user.role != UserRole.DOCTOR:
        raise ValueError("Selected user does not have a doctor role")

    # Prevent duplicate doctor profiles
    existing_doctor = doctor_repository.get_doctor_by_user_id(
        db, doctor_data.user_id
    )

    if existing_doctor:
        raise ValueError("Doctor profile already exists for this user")

    new_doctor = Doctor(
        user_id=doctor_data.user_id,
        specialization=doctor_data.specialization,
        qualification=doctor_data.qualification,
        experience_years=doctor_data.experience_years,
        consultation_fee=doctor_data.consultation_fee,
        bio=doctor_data.bio,
        is_available=doctor_data.is_available
    )

    try:
        return doctor_repository.create_doctor(db, new_doctor)
    except Exception:
        db.rollback()
        raise


def get_all_doctors(db: Session):
    return doctor_repository.get_all_doctors(db)


def get_doctor_by_id(db: Session, doctor_id: int):
    doctor = doctor_repository.get_doctor_by_id(
        db, doctor_id
    )

    if doctor is None:
        raise ValueError("Doctor not found")

    return doctor


def update_doctor(
    db: Session,
    doctor_id: int,
    doctor_data: DoctorUpdate
):
    doctor = doctor_repository.get_doctor_by_id(
        db, doctor_id
    )

    if doctor is None:
        raise ValueError("Doctor not found")

    update_data = doctor_data.model_dump(exclude_unset=True)

    # Do not assign None to required database fields
    for field, value in update_data.items():
        if value is None and field != "bio":
            raise ValueError(f"{field} cannot be null")

    try:
        return doctor_repository.update_doctor(
            db, doctor, update_data
        )
    except Exception:
        db.rollback()
        raise


def delete_doctor(db: Session, doctor_id: int):
    doctor = doctor_repository.get_doctor_by_id(
        db, doctor_id
    )

    if doctor is None:
        raise ValueError("Doctor not found")

    # Preserve doctors who have appointment history
    if doctor.appointments:
        raise ValueError(
            "Cannot delete doctor with existing appointments"
        )

    try:
        doctor_repository.delete_doctor(db, doctor)
    except Exception:
        db.rollback()
        raise

    return {"message": "Doctor deleted successfully"}
