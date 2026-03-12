from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from modules.create.api.schemas import CreateUserSchema, RegisterResponseSchema, EmailSchema
from modules.register.application.register_user_service import register_user
from database.session import get_db
from common.exceptions import http_500
from common.services.email import EmailService



router = APIRouter()


@router.post("", summary="Register a new user", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseSchema)
def register_user_route(payload: CreateUserSchema, background: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        user = register_user(
            db=db,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password
        )

        return {
            "message": "Successfully created user. Ask for an admin to approve your request.",
            "user": user
        }

    except Exception as e:
        raise http_500("Internal error while creating user", e)

