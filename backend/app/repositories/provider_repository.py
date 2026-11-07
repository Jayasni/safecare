from sqlalchemy.orm import Session

from app.models.provider import Provider


class ProviderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, provider_id: int) -> Provider | None:
        return self.db.get(Provider, provider_id)

    def list(self, active_only: bool = True) -> list[Provider]:
        query = self.db.query(Provider)
        if active_only:
            query = query.filter(Provider.is_active.is_(True))
        return query.order_by(Provider.full_name).all()

    def create(self, provider: Provider) -> Provider:
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def update(self, provider: Provider) -> Provider:
        self.db.commit()
        self.db.refresh(provider)
        return provider