from sqlalchemy.orm import Session
from database.models.users import Users
from common.exceptions import http_404, http_400


def verify_user_email(db: Session, user_id: int):
    """Mark user email as verified"""
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise http_404("User not found.")
    
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str, must_be_unverified: bool = False):
    """Retrieve a user by email with optional unverified check"""
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise http_404("User not found.")
    
    if must_be_unverified and user.is_verified:
        raise http_400("User already verified.")
    return user

