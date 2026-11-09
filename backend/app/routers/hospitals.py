
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies_auth import require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.hospital import (
    HospitalCreate,
    HospitalUpdate,
    HospitalResponse,
)
from app.services import hospital_service


router = APIRouter(
    prefix="/api/v1/hospitals",
    tags=["Hospitals"]
)


# 1. Get all active hospitals - Public
@router.get(
    "/",
    response_model=list[HospitalResponse]
)
def get_all_hospitals(
    db: Session = Depends(get_db)
):
    return hospital_service.get_all_hospitals(db)


# 2. Get hospital by ID - Public
@router.get(
    "/{hospital_id}",
    response_model=HospitalResponse
)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):
    try:
        return hospital_service.get_hospital_by_id(
            db, hospital_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# 3. Create hospital - Admin only
@router.post(
    "/",
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED
)
def create_hospital(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return hospital_service.create_hospital(
            db, hospital_data
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create hospital"
        )


# 4. Update hospital - Admin only
@router.patch(
    "/{hospital_id}",
    response_model=HospitalResponse
)
def update_hospital(
    hospital_id: int,
    hospital_data: HospitalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return hospital_service.update_hospital(
            db, hospital_id, hospital_data
        )
    except ValueError as error:
        message = str(error)

        code = (
            status.HTTP_404_NOT_FOUND
            if message == "Hospital not found"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=code,
            detail=message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update hospital"
        )


# 5. Deactivate hospital - Admin only
@router.delete(
    "/{hospital_id}",
    status_code=status.HTTP_200_OK
)
def delete_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    )
):
    try:
        return hospital_service.deactivate_hospital(
            db, hospital_id
        )
    except ValueError as error:
        message = str(error)

        code = (
            status.HTTP_404_NOT_FOUND
            if message == "Hospital not found"
            else status.HTTP_409_CONFLICT
        )

        raise HTTPException(
            status_code=code,
            detail=message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to deactivate hospital"
        )
