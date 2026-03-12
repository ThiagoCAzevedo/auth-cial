from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.update.application.update_user_service import update_user
from database.session import get_db
from common.exceptions import http_500
from common.services.user import ensure_is_admin
from common.logger import logger


log = logger("update_api")


router = APIRouter()


@router.put("/{user_id}", summary="Update a user", dependencies=[Depends(ensure_is_admin)])
def update_user_route(user_id: int, payload: dict, db: Session = Depends(get_db)):
    log.info(f"Update request for user: {user_id}")
    try:
        updated = update_user(db, user_id, **payload)
        log.info(f"User updated successfully: {user_id}")
        return updated
    except Exception as e:
        log.error(f"Error updating user {user_id}: {str(e)}", exc_info=True)
        raise http_500("Erro ao atualizar usuário: ", e)

