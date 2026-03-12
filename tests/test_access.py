import pytest
from fastapi import HTTPException
from modules.register.application.register_user_service import register_user
from modules.update.application.update_user_service import update_user
from common.security.password import verify_password
from common.security.jwt import create_access_token, create_refresh_token, verify_token
from datetime import datetime, timedelta, timezone
import jwt


class TestAuthentication:
    def test_successful_login(self, db_session):
        """Test successful user login"""
        # Create a test user
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "TestPass123!"
        }

        user = register_user(db=db_session, **user_data)

        # Verify the user
        user.is_verified = True
        db_session.commit()

        # Test password verification
        assert verify_password(user_data["password"], user.password)

        # Test JWT token creation
        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        assert access_token is not None
        assert refresh_token is not None

        # Test token verification
        decoded = verify_token(access_token, token_type="access")
        assert decoded["sub"] == str(user.id)
        assert decoded["email"] == user.email
        assert decoded["type"] == "access"

    def test_login_unverified_user(self, db_session):
        """Test login attempt with unverified user"""
        # Create unverified user
        user_data = {
            "first_name": "Unverified",
            "last_name": "User",
            "email": "unverified@example.com",
            "password": "TestPass123!"
        }

        user = register_user(db=db_session, **user_data)
        assert user.is_verified == False

        # This would be tested in the API layer, but we can verify the state
        assert not user.is_verified

    def test_invalid_password(self, db_session):
        """Test login with invalid password"""
        # Create a test user
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test2@example.com",
            "password": "CorrectPass123!"
        }

        user = register_user(db=db_session, **user_data)
            
        with pytest.raises(HTTPException):
            verify_password("WrongPassword", user.password)

    def test_token_expiry(self, db_session):
        """Test token expiry handling"""

        # Create expired token manually (this is a simplified test)
        expired_data = {
            "sub": "1",
            "email": "test@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),  # Already expired
            "type": "access"
        }

        # This would normally be caught by JWT library
        # We test the exception handling
        try:
            token = jwt.encode(expired_data, "secret", algorithm="HS256")
            # Verification should fail
            with pytest.raises(HTTPException):
                verify_token(token)
        except ImportError:
            pass  # Skip if jwt not available in test

    def test_refresh_token_storage(self, db_session):
        """Test refresh token storage in user record"""
        # Create a test user
        user_data = {
            "first_name": "Refresh",
            "last_name": "Test",
            "email": "refresh@example.com",
            "password": "TestPass123!"
        }

        user = register_user(db=db_session, **user_data)

        # Update with refresh token
        refresh_token = "test_refresh_token_123"
        update_user(db=db_session, user_id=user.id, refresh_token=refresh_token)

        # Verify token was stored
        db_session.refresh(user)
        assert user.refresh_token == refresh_token

        # Test clearing refresh token (logout)
        update_user(db=db_session, user_id=user.id, refresh_token=None)
        db_session.refresh(user)
        assert user.refresh_token is None

