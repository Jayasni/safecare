from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

REFRESH_COOKIE_NAME = "refresh_token"


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        path="/",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register(user_create)


@router.post("/login", response_model=TokenResponse)
def login(
    user_login: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    access_token, refresh_token, user = auth_service.login(
        user_login.email, user_login.password
    )
    set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token, user=user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    access_token, refresh_token, user = auth_service.refresh_access_token(raw_refresh_token)
    set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token, user=user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    auth_service.logout(request.cookies.get(REFRESH_COOKIE_NAME))
    clear_refresh_cookie(response)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user