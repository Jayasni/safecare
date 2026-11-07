from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.availability_slot import AvailabilitySlot
from app.models.provider import Provider
from app.models.service import Service
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.provider_repository import ProviderRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.availability import AvailabilitySlotCreate, AvailabilitySlotUpdate


class AvailabilityService:
    def __init__(self, db: Session):
        self.db = db
        self.slots = AvailabilityRepository(db)
        self.services = ServiceRepository(db)
        self.providers = ProviderRepository(db)

    def _active_service(self, service_id: int) -> Service:
        service = self.services.get_by_id(service_id)
        if service is None:
            raise HTTPException(status_code=404, detail="Service not found")
        if not service.is_active:
            raise HTTPException(status_code=400, detail="Inactive services cannot be used")
        return service

    def _active_provider(self, provider_id: int | None) -> Provider | None:
        if provider_id is None:
            return None
        provider = self.providers.get_by_id(provider_id)
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        if not provider.is_active:
            raise HTTPException(status_code=400, detail="Inactive providers cannot be used")
        return provider

    def list_slots(self, **kwargs):
        return self.slots.list(**kwargs)

    def get_slot(self, slot_id: int):
        slot = self.slots.get_by_id(slot_id)
        if slot is None:
            raise HTTPException(status_code=404, detail="Availability slot not found")
        return slot

    def create_slot(self, payload: AvailabilitySlotCreate):
        if payload.end_time <= payload.start_time:
            raise HTTPException(status_code=400, detail="End time must be after start time")
        if payload.start_time <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Cannot create a slot in the past")

        self._active_service(payload.service_id)
        self._active_provider(payload.provider_id)

        if payload.provider_id is not None and self.slots.has_conflict(
            provider_id=payload.provider_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
        ):
            raise HTTPException(
                status_code=409, detail="This provider already has a conflicting slot"
            )

        slot = AvailabilitySlot(
            service_id=payload.service_id,
            provider_id=payload.provider_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
            capacity=payload.capacity,
            is_active=payload.is_active,
        )
        return self.slots.create(slot)

    def update_slot(self, slot_id: int, payload: AvailabilitySlotUpdate):
        slot = self.get_slot(slot_id)
        data = payload.model_dump(exclude_unset=True)

        new_service_id = data.get("service_id", slot.service_id)
        new_provider_id = data.get("provider_id", slot.provider_id)
        new_start = data.get("start_time", slot.start_time)
        new_end = data.get("end_time", slot.end_time)
        new_capacity = data.get("capacity", slot.capacity)

        if new_end <= new_start:
            raise HTTPException(status_code=400, detail="End time must be after start time")

        active_bookings = self.slots.active_booking_count(slot.id)
        if new_capacity is not None and new_capacity < active_bookings:
            raise HTTPException(
                status_code=400,
                detail="Capacity cannot be lower than existing active bookings",
            )

        if new_service_id != slot.service_id:
            self._active_service(new_service_id)
        if new_provider_id != slot.provider_id:
            self._active_provider(new_provider_id)

        if new_provider_id is not None:
            if self.slots.has_conflict(
                provider_id=new_provider_id,
                start_time=new_start,
                end_time=new_end,
                exclude_slot_id=slot.id,
            ):
                raise HTTPException(
                    status_code=409, detail="This provider already has a conflicting slot"
                )

        slot.service_id = new_service_id
        slot.provider_id = new_provider_id
        slot.start_time = new_start
        slot.end_time = new_end
        if new_capacity is not None:
            slot.capacity = new_capacity
        if "is_active" in data:
            if data["is_active"] is False and active_bookings > 0:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot deactivate a slot with active bookings",
                )
            slot.is_active = data["is_active"]

        return self.slots.update(slot)

    def set_slot_status(self, slot_id: int, is_active: bool):
        slot = self.get_slot(slot_id)
        active_bookings = self.slots.active_booking_count(slot.id)
        if is_active is False and active_bookings > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot deactivate a slot with active bookings",
            )
        slot.is_active = is_active
        return self.slots.update(slot)