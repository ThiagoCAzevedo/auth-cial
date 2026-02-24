from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from helpers.security.password import UserPassword
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.jwt import JWTHandler

class RegisterUsers:

    @staticmethod
    def create_user(
        db: Session, 
        first_name: str, 
        last_name: str, 
        email: str, 
        password: str, 
    ):
        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=UserPassword.hash_password(password),
            is_verified=False
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTP_Exceptions.http_400("E-mail already exists.")
        
        verification_token = JWTHandler.create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "purpose": "email_verification"
        })

        return user, verification_token