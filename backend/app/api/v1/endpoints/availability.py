from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.availability import (
    AvailabilitySlotCreate,
    AvailabilitySlotResponse,
    AvailabilitySlotUpdate,
)
from app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/availability", tags=["Availability"])


@router.get("", response_model=list[AvailabilitySlotResponse])
def list_availability(
    service_id: int | None = Query(default=None),
    provider_id: int | None = Query(default=None),
    upcoming_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    return AvailabilityService(db).list_slots(
        service_id=service_id,
        provider_id=provider_id,
        active_only=True,
        upcoming_only=upcoming_only,
    )


@router.get("/{slot_id}", response_model=AvailabilitySlotResponse)
def get_availability(slot_id: int, db: Session = Depends(get_db)):
    service = AvailabilityService(db)
    try:
        return service.get_slot(slot_id)
    except HTTPException:
        raise


@router.post("", response_model=AvailabilitySlotResponse, status_code=status.HTTP_201_CREATED)
def create_availability(
    payload: AvailabilitySlotCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return AvailabilityService(db).create_slot(payload)


@router.patch("/{slot_id}", response_model=AvailabilitySlotResponse)
def update_availability(
    slot_id: int,
    payload: AvailabilitySlotUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return AvailabilityService(db).update_slot(slot_id, payload)


@router.patch("/{slot_id}/status", response_model=AvailabilitySlotResponse)
def set_availability_status(
    slot_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return AvailabilityService(db).set_slot_status(slot_id, is_active)