from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from helpers.users import UserPassword, UserValidators
from fastapi import HTTPException

class RegisterUsers:

    @staticmethod
    def create_user(
        db: Session, 
        first_name: str, 
        last_name: str, 
        email: str, 
        password: str, 
    ) -> Users:

        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=UserPassword.hash_password(password)
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="E-mail already exists.")
        
        return user