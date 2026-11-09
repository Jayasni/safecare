
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.user import User


def get_all_doctors(db: Session):
    return db.query(Doctor).all()


def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()


def get_doctor_by_user_id(db: Session, user_id: int):
    return db.query(Doctor).filter(
        Doctor.user_id == user_id
    ).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def create_doctor(db: Session, doctor: Doctor):
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor(db: Session, doctor: Doctor, update_data: dict):
    for field, value in update_data.items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor: Doctor):
    db.delete(doctor)
    db.commit()
