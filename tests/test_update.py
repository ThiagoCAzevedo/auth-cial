from modules.register.application.register_user_service import register_user
from modules.update.application.update_user_service import update_user
import pytest


class TestUpdateUser:
    def test_update_user_fields(self, db_session):
        user_data = {
            "first_name": "Original",
            "last_name": "Name",
            "email": "original@example.com",
            "password": "OriginalPass123!"
        }

        user = register_user(db=db_session, **user_data)

        update_data = {
            "first_name": "Updated",
            "last_name": "Surname",
            "status": True
        }

        updated_user = update_user(db=db_session, user_id=user.id, **update_data)

        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Surname"
        assert updated_user.status == True
        assert updated_user.email == user_data["email"]

    def test_update_refresh_token(self, db_session):
        user_data = {
            "first_name": "Token",
            "last_name": "User",
            "email": "token@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        refresh_token = "new_refresh_token_12345"
        updated_user = update_user(db=db_session, user_id=user.id, refresh_token=refresh_token)

        assert updated_user.refresh_token == refresh_token

        updated_user = update_user(db=db_session, user_id=user.id, refresh_token=None)
        assert updated_user.refresh_token is None

    def test_update_nonexistent_user(self, db_session):
        with pytest.raises(Exception) as exc_info:
            update_user(db=db_session, user_id=99999, first_name="Test")

        assert "User not found" in str(exc_info.value)

    def test_partial_update(self, db_session):
        user_data = {
            "first_name": "Partial",
            "last_name": "Update",
            "email": "partial@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        updated_user = update_user(db=db_session, user_id=user.id, first_name="Partially")

        assert updated_user.first_name == "Partially"
        assert updated_user.last_name == "Update"
        assert updated_user.email == "partial@example.com"

    def test_update_user_role(self, db_session):
        user_data = {
            "first_name": "Role",
            "last_name": "Test",
            "email": "role@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)

        updated_user = update_user(db=db_session, user_id=user.id, role="admin")
        assert updated_user.role == "admin"

        updated_user = update_user(db=db_session, user_id=user.id, role="user")
        assert updated_user.role == "user"

    def test_update_user_verification_status(self, db_session):
        user_data = {
            "first_name": "Verify",
            "last_name": "Test",
            "email": "verify@example.com",
            "password": "Pass123!"
        }

        user = register_user(db=db_session, **user_data)
        assert user.is_verified == False

        updated_user = update_user(db=db_session, user_id=user.id, is_verified=True)
        assert updated_user.is_verified == True

        updated_user = update_user(db=db_session, user_id=user.id, is_verified=False)
        assert updated_user.is_verified == False