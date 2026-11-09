
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import UserRole
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.repositories import user_repository


def register_user(db: Session, user_data: UserCreate):
    # Check whether the email already exists
    existing_user = user_repository.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise ValueError("Email is already registered")

    # Hash the password before storing it
    hashed_password = hash_password(user_data.password)

    # Public registration always creates a patient account
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password,
        role=UserRole.PATIENT
    )

    # Save the user in PostgreSQL
    return user_repository.create_user(db, new_user)
