from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from common.security.password import hash_password
from common.exceptions import http_400
from common.logger import logger


log = logger("register_service")


def register_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    if not first_name:
        raise Exception("First name is required")

    if not last_name:
        raise Exception("Last name is required")

    if not email:
        raise Exception("Email is required")

    if not password:
        raise Exception("Password is required")

    log.debug(f"Creating user: {email}")
    user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hash_password(password),
        is_verified=False
    )

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        log.info(f"User created successfully: {user.id} - {email}")
    except IntegrityError:
        db.rollback()
        log.warning(f"User creation failed - email already exists: {email}")
        raise http_400("E-mail already exists.")

    return user

