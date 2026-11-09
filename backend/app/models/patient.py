from datetime import date

from sqlalchemy import (
    String,
    Date,
    Text,
    ForeignKey,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import Gender


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    gender: Mapped[Gender | None] = mapped_column(
        SQLAlchemyEnum(
            Gender,
            name="patient_gender",
            values_callable=lambda enum: [item.value for item in enum],
            native_enum=False
        ),
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    emergency_contact: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="patient_profile"
    )

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )