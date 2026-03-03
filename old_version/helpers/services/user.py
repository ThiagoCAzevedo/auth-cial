from fastapi import Depends
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.dependencies import get_current_user
from sqlalchemy.orm import Session
from database.models.users import Users


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, current_user_id: int):
        user = db.query(Users).filter(Users.id == current_user_id).first()
        if not user:
            raise HTTP_Exceptions.http_404("User not found.")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, current_user_email: int, verify_user: bool = False):
        user = db.query(Users).filter(Users.email == current_user_email).first()
        if not user:
            raise HTTP_Exceptions.http_404("User not found.")
        
        if verify_user and user.is_verified:
            raise HTTP_Exceptions.http_400("User already verified.")
        return user

    @staticmethod
    def ensure_is_admin(current_user = Depends(get_current_user)):
        if current_user["role"] != "admin":
            raise HTTP_Exceptions.http_403("Access only for admins")
        return True
