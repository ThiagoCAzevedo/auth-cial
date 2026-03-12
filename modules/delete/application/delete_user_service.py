from sqlalchemy.orm import Session
from fastapi import HTTPException
from modules.delete.infrastructure.repositories import UserDeleteRepository
from common.logger import logger


log = logger("delete_service")


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user via repository; raise if not found."""
    log.debug(f"Deleting user: {user_id}")
    try:
        result = UserDeleteRepository().delete_user(db, user_id)
        log.info(f"User deleted successfully: {user_id}")
        return result
    except Exception as e:
        log.error(f"Failed to delete user {user_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="User not found.")

