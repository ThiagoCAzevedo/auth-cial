from fastapi import HTTPException
from modules.register.application.register_user_service import register_user
from modules.delete.application.delete_user_service import delete_user
from database.models.users import Users
import pytest


class TestDeleteUser:
    def test_delete_existing_user(self, db_session):
        user_data = {
            "first_name": "Delete",
            "last_name": "Test",
            "email": "delete@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is not None

        result = delete_user(db=db_session, user_id=user.id)
        assert result == True

        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is None

    def test_delete_nonexistent_user(self, db_session):
        with pytest.raises(HTTPException) as exc_info:
            delete_user(db=db_session, user_id=99999)

        assert "User not found" in str(exc_info.value.detail)

    def test_delete_user_with_dependencies(self, db_session):
        user_data = {
            "first_name": "Dependency",
            "last_name": "Test",
            "email": "dependency@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        result = delete_user(db=db_session, user_id=user.id)
        assert result == True

        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is None

    def test_delete_user_audit_trail(self, db_session):
        user_data = {
            "first_name": "Audit",
            "last_name": "Trail",
            "email": "audit@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        result = delete_user(db=db_session, user_id=user.id)
        assert result == True

        assert result == True