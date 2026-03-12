from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.access.api.schemas import (
    UserResponseSchema, LoginUserSchema, LoginResponseSchema,
    RefreshTokenSchema
)
# the update functionality has been moved to its own module
from modules.update.application.update_user_service import update_user
from database.session import get_db
from common.exceptions import http_403
from common.security.password import verify_password
from common.security.jwt import create_access_token, create_refresh_token, verify_token
from common.security.dependencies import get_current_user
from common.services.user import get_user_by_id, get_user_by_email
from common.logger import logger


log = logger("access_api")


router = APIRouter()


@router.get("/me", summary="Return logged user", response_model=UserResponseSchema)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(current_user["sub"])
    log.debug(f"Fetching current user profile: {user_id}")
    user = get_user_by_id(db, user_id)
    log.info(f"User profile retrieved: {user_id} - {user.email}")
    return user


@router.post("/login", summary="Login user", response_model=LoginResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    log.info(f"Login attempt for email: {payload.email}")
    
    user = get_user_by_email(db, payload.email)
    
    if not user.is_verified:
        log.warning(f"Login blocked - unverified account: {payload.email}")
        raise http_403("Conta não verificada. Por favor, solicite a um administrador para verificar seu e-mail antes de fazer login.")
    
    try:
        verify_password(payload.password, user.password)
        log.info(f"Login successful for user: {user.id} - {user.email}")
    except Exception as e:
        log.warning(f"Login failed - invalid password for email: {payload.email}")
        raise e

    refresh_days = 30 if payload.remember_me else 1
    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id), "email": user.email, "role": user.role},
        expires_days=refresh_days
    )

    update_user(db, user.id, refresh_token=refresh_token)

    log.debug(f"Tokens generated for user: {user.id}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "remember_me": payload.remember_me,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout", summary="Logout user")
def logout_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(current_user["sub"])
    log.info(f"Logout request for user: {user_id}")
    update_user(db, user_id, refresh_token=None)
    log.info(f"User logged out successfully: {user_id}")
    return {"message": "Successfully logout user"}

