
from sqlalchemy.orm import Session

from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from app.repositories import hospital_repository


def create_hospital(db: Session, hospital_data: HospitalCreate):
    new_hospital = Hospital(
        name=hospital_data.name,
        description=hospital_data.description,
        address=hospital_data.address,
        city=hospital_data.city,
        state=hospital_data.state,
        postal_code=hospital_data.postal_code,
        phone=hospital_data.phone,
        email=hospital_data.email,
        is_active=True,
    )

    try:
        return hospital_repository.create_hospital(
            db, new_hospital
        )
    except Exception:
        db.rollback()
        raise


def get_all_hospitals(db: Session):
    return hospital_repository.get_all_hospitals(db)


def get_hospital_by_id(db: Session, hospital_id: int):
    hospital = hospital_repository.get_hospital_by_id(
        db, hospital_id
    )

    if hospital is None or not hospital.is_active:
        raise ValueError("Hospital not found")

    return hospital


def update_hospital(
    db: Session,
    hospital_id: int,
    hospital_data: HospitalUpdate
):
    hospital = hospital_repository.get_hospital_by_id(
        db, hospital_id
    )

    if hospital is None:
        raise ValueError("Hospital not found")

    update_data = hospital_data.model_dump(exclude_unset=True)

    # Required database fields cannot be set to null.
    required_fields = {
        "name",
        "address",
        "city",
        "state",
        "phone",
        "is_active",
    }

    for field, value in update_data.items():
        if value is None and field in required_fields:
            raise ValueError(f"{field} cannot be null")

    try:
        return hospital_repository.update_hospital(
            db, hospital, update_data
        )
    except Exception:
        db.rollback()
        raise


def deactivate_hospital(db: Session, hospital_id: int):
    hospital = hospital_repository.get_hospital_by_id(
        db, hospital_id
    )

    if hospital is None:
        raise ValueError("Hospital not found")

    if not hospital.is_active:
        raise ValueError("Hospital is already inactive")

    try:
        hospital_repository.deactivate_hospital(db, hospital)
        return {"message": "Hospital deactivated successfully"}
    except Exception:
        db.rollback()
        raise
