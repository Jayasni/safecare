from sqlalchemy.orm import Session

from app.models.service import Service


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, service_id: int) -> Service | None:
        return self.db.get(Service, service_id)

    def list(self, active_only: bool = True) -> list[Service]:
        query = self.db.query(Service)
        if active_only:
            query = query.filter(Service.is_active.is_(True))
        return query.order_by(Service.name).all()

    def create(self, service: Service) -> Service:
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def update(self, service: Service) -> Service:
        self.db.commit()
        self.db.refresh(service)
        return service