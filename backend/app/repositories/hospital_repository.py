
from sqlalchemy.orm import Session

from app.models.hospital import Hospital


def get_all_hospitals(db: Session):
    return (
        db.query(Hospital)
        .filter(Hospital.is_active.is_(True))
        .order_by(Hospital.name)
        .all()
    )


def get_hospital_by_id(db: Session, hospital_id: int):
    return (
        db.query(Hospital)
        .filter(Hospital.id == hospital_id)
        .first()
    )


def create_hospital(db: Session, hospital: Hospital):
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


def update_hospital(
    db: Session,
    hospital: Hospital,
    update_data: dict
):
    for field, value in update_data.items():
        setattr(hospital, field, value)

    db.commit()
    db.refresh(hospital)
    return hospital


def deactivate_hospital(db: Session, hospital: Hospital):
    hospital.is_active = False
    db.commit()
    db.refresh(hospital)
    return hospital
