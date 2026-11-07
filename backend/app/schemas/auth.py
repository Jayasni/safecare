from pydantic import EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import ORMModel
from app.schemas.user import UserResponse


class UserLogin(ORMModel):
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(ORMModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AuthMeResponse(ORMModel):
    user: UserResponse