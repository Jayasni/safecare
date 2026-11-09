
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.auth import LoginRequest
from app.core.security import verify_password, create_access_token


def login_user(db: Session, login_data: LoginRequest):
    # Step 1: Find user by email
    user = user_repository.get_user_by_email(
        db,
        login_data.email
    )

    # Step 2: Check user and password
    if not user or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise ValueError("Invalid email or password")

    # Step 3: Check whether account is active
    if not user.is_active:
        raise ValueError("This account is inactive")

    # Step 4: Generate JWT access token
    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })

    # Step 5: Return token and user
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
