from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_optional_current_user, require_admin
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.provider import ProviderCreate, ProviderResponse, ProviderUpdate
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.services.service_service import ServiceService

router = APIRouter(tags=["Services and Providers"])


def handle_value_error(exc: ValueError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# Services
@router.get("/services", response_model=list[ServiceResponse])
def list_services(
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user),
):
    is_admin = current_user is not None and current_user.role == UserRole.admin
    if active_only is False and not is_admin:
        active_only = True
    return ServiceService(db).list_services(active_only=active_only)


@router.get("/services/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = ServiceService(db)
    try:
        return service.get_service(service_id)
    except ValueError as exc:
        handle_value_error(exc)


@router.post("/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    payload: ServiceCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return ServiceService(db).create_service(payload)


@router.patch("/services/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    payload: ServiceUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = ServiceService(db)
    try:
        return service.update_service(service_id, payload)
    except ValueError as exc:
        handle_value_error(exc)


@router.patch("/services/{service_id}/status", response_model=ServiceResponse)
def set_service_status(
    service_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = ServiceService(db)
    try:
        return service.set_service_status(service_id, is_active)
    except ValueError as exc:
        handle_value_error(exc)


# Providers
@router.get("/providers", response_model=list[ProviderResponse])
def list_providers(
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    return ServiceService(db).list_providers(active_only=active_only)


@router.get("/providers/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    service = ServiceService(db)
    try:
        return service.get_provider(provider_id)
    except ValueError as exc:
        handle_value_error(exc)


@router.post("/providers", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
def create_provider(
    payload: ProviderCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return ServiceService(db).create_provider(payload)


@router.patch("/providers/{provider_id}", response_model=ProviderResponse)
def update_provider(
    provider_id: int,
    payload: ProviderUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = ServiceService(db)
    try:
        return service.update_provider(provider_id, payload)
    except ValueError as exc:
        handle_value_error(exc)


@router.patch("/providers/{provider_id}/status", response_model=ProviderResponse)
def set_provider_status(
    provider_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = ServiceService(db)
    try:
        return service.set_provider_status(provider_id, is_active)
    except ValueError as exc:
        handle_value_error(exc)