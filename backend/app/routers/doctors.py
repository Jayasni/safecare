
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies_auth import require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse
)
from app.services import doctor_service


router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"]
)


# 1. Get all doctors - Public
@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def get_all_doctors(
    db: Session = Depends(get_db)
):
    return doctor_service.get_all_doctors(db)


# 2. Get doctor by ID - Public
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    try:
        return doctor_service.get_doctor_by_id(
            db, doctor_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# 3. Create doctor - Admin only
@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return doctor_service.create_doctor(
            db, doctor_data
        )
    except ValueError as error:
        message = str(error)

        if "already exists" in message:
            code = status.HTTP_409_CONFLICT
        elif "not found" in message:
            code = status.HTTP_404_NOT_FOUND
        else:
            code = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=code,
            detail=message
        )


# 4. Update doctor - Admin only
@router.patch(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return doctor_service.update_doctor(
            db, doctor_id, doctor_data
        )
    except ValueError as error:
        message = str(error)

        code = (
            status.HTTP_404_NOT_FOUND
            if message == "Doctor not found"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=code,
            detail=message
        )


# 5. Delete doctor - Admin only
@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_200_OK
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return doctor_service.delete_doctor(
            db, doctor_id
        )
    except ValueError as error:
        message = str(error)

        code = (
            status.HTTP_404_NOT_FOUND
            if message == "Doctor not found"
            else status.HTTP_409_CONFLICT
        )

        raise HTTPException(
            status_code=code,
            detail=message
        )
