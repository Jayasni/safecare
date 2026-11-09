
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DoctorHospitalService(Base):
    __tablename__ = "doctor_hospital_services"

    __table_args__ = (
        UniqueConstraint(
            "doctor_hospital_id",
            "service_id",
            name="uq_doctor_hospital_service"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    doctor_hospital_id: Mapped[int] = mapped_column(
        ForeignKey("doctor_hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("medical_services.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    doctor_hospital = relationship(
        "DoctorHospital",
        back_populates="services"
    )

    service = relationship(
        "MedicalService",
        back_populates="doctor_assignments"
    )
