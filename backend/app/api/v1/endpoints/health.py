from fastapi import APIRouter

from app.db.session import check_database_connection

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {"success": True, "message": "Service Booking API is running", "data": {"status": "ok"}}


@router.get("/health/db")
def database_health_check():
    check_database_connection()
    return {"success": True, "message": "Database connection is working", "data": {"status": "ok"}}