
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import Base, engine
from app import models
from app.core.config import settings
from app.dependencies import get_db


from app.routers import auth, admin,doctors,hospitals
app = FastAPI(
    title=settings.APP_NAME,
    description="Healora Healthcare Appointment Booking API",
    version="1.0.0"
)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(doctors.router)
app.include_router(hospitals.router)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to Healora API",
        "status": "running"
    }


# Health check
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Healora"
    }

@app.get("/api/v1/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "success",
            "database": "PostgreSQL connected successfully"
        }

    except Exception as error:
        print("DATABASE ERROR:", type(error).__name__, str(error))

        return {
            "status": "error",
            "message": "Database connection failed. Check terminal."
        }

@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)
    print("Healora database tables created successfully!")