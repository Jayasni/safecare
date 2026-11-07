import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.refresh_tokens = RefreshTokenRepository(db)

    @staticmethod
    def hash_refresh_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_refresh_token() -> str:
        return secrets.token_urlsafe(48)

    def register(self, user_create: UserCreate) -> User:
        if self.users.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        user = User(
            full_name=user_create.full_name,
            email=user_create.email,
            password_hash=hash_password(user_create.password),
            phone=user_create.phone,
            role=UserRole.customer,
        )
        return self.users.create(user)

    def login(self, email: str, password: str) -> tuple[str, str, User]:
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive",
            )

        access_token = create_access_token(user.id)
        refresh_token = self.generate_refresh_token()
        self.refresh_tokens.create(
            user_id=user.id,
            token_hash=self.hash_refresh_token(refresh_token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return access_token, refresh_token, user

    def refresh_access_token(self, raw_refresh_token: str | None) -> tuple[str, str, User]:
        if not raw_refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is missing",
            )

        record = self.refresh_tokens.get_by_hash(self.hash_refresh_token(raw_refresh_token))
        now = datetime.now(timezone.utc)

        if (
            record is None
            or record.revoked_at is not None
            or record.expires_at <= now
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid or expired",
            )

        user = self.users.get_by_id(record.user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        self.refresh_tokens.revoke(record, now)

        new_refresh_token = self.generate_refresh_token()
        self.refresh_tokens.create(
            user_id=user.id,
            token_hash=self.hash_refresh_token(new_refresh_token),
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        access_token = create_access_token(user.id)
        return access_token, new_refresh_token, user

    def logout(self, raw_refresh_token: str | None) -> None:
        if not raw_refresh_token:
            return

        record = self.refresh_tokens.get_by_hash(self.hash_refresh_token(raw_refresh_token))
        if record is not None and record.revoked_at is None:
            self.refresh_tokens.revoke(record)