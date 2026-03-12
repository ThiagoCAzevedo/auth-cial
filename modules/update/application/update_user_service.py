from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models.users import Users
from common.logger import logger


log = logger("update_service")


def update_user(db: Session, user_id: int, **fields):
    """Update the specified fields on a user record."""
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in fields.items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

