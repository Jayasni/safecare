from fastapi import APIRouter

from app.api.v1.endpoints import availability, auth, health, services

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(services.router)
api_v1_router.include_router(availability.router)