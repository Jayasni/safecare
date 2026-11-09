
"""add multi hospital support

Revision ID: 9e63432335dd
Revises:
Create Date: 2026-11-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9e63432335dd"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add hospital and service references to appointments.
    op.add_column(
        "appointments",
        sa.Column("hospital_id", sa.Integer(), nullable=False),
    )

    op.add_column(
        "appointments",
        sa.Column("service_id", sa.Integer(), nullable=False),
    )

    # Add indexes.
    op.create_index(
        "ix_appointments_hospital_id",
        "appointments",
        ["hospital_id"],
        unique=False,
    )

    op.create_index(
        "ix_appointments_service_id",
        "appointments",
        ["service_id"],
        unique=False,
    )

    # Add foreign keys.
    op.create_foreign_key(
        "fk_appointments_hospital_id_hospitals",
        "appointments",
        "hospitals",
        ["hospital_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_appointments_service_id_medical_services",
        "appointments",
        "medical_services",
        ["service_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_appointments_service_id_medical_services",
        "appointments",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_appointments_hospital_id_hospitals",
        "appointments",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_appointments_service_id",
        table_name="appointments",
    )

    op.drop_index(
        "ix_appointments_hospital_id",
        table_name="appointments",
    )

    op.drop_column("appointments", "service_id")
    op.drop_column("appointments", "hospital_id")
