from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from helpers.security.dependencies import get_current_user
from services.update import UpdateUsers


router = APIRouter()


@router.post("", summary="Logout user")
def logout_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    UpdateUsers.update_user(db, current_user["sub"], refresh_token=None)
    return {"message": "Successfully logout user"}