from sqlalchemy.orm import Session

from app.models.service import Service
from app.models.provider import Provider
from app.repositories.service_repository import ServiceRepository
from app.repositories.provider_repository import ProviderRepository
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.schemas.provider import ProviderCreate, ProviderUpdate


class ServiceService:
    def __init__(self, db: Session):
        self.db = db
        self.services = ServiceRepository(db)
        self.providers = ProviderRepository(db)

    # Services
    def list_services(self, active_only: bool = True):
        return self.services.list(active_only=active_only)

    def get_service(self, service_id: int):
        service = self.services.get_by_id(service_id)
        if service is None:
            raise ValueError("Service not found")
        return service

    def create_service(self, payload: ServiceCreate) -> Service:
        service = Service(**payload.model_dump())
        return self.services.create(service)

    def update_service(self, service_id: int, payload: ServiceUpdate) -> Service:
        service = self.get_service(service_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(service, field, value)
        return self.services.update(service)

    def set_service_status(self, service_id: int, is_active: bool) -> Service:
        service = self.get_service(service_id)
        service.is_active = is_active
        return self.services.update(service)

    # Providers
    def list_providers(self, active_only: bool = True):
        return self.providers.list(active_only=active_only)

    def get_provider(self, provider_id: int):
        provider = self.providers.get_by_id(provider_id)
        if provider is None:
            raise ValueError("Provider not found")
        return provider

    def create_provider(self, payload: ProviderCreate) -> Provider:
        provider = Provider(**payload.model_dump())
        return self.providers.create(provider)

    def update_provider(self, provider_id: int, payload: ProviderUpdate) -> Provider:
        provider = self.get_provider(provider_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(provider, field, value)
        return self.providers.update(provider)

    def set_provider_status(self, provider_id: int, is_active: bool) -> Provider:
        provider = self.get_provider(provider_id)
        provider.is_active = is_active
        return self.providers.update(provider)