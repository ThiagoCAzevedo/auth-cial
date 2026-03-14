from fastapi import HTTPException
from common.security.password import hash_password, verify_password
from common.security.jwt import create_access_token, create_refresh_token, verify_token, create_password_reset_token
from common.services.validators import validate_password, validate_email_domain
import pytest


class TestPasswordSecurity:
    def test_password_hashing(self):
        password = "MySecurePassword123!"

        hashed = hash_password(password)
        assert hashed != password
        assert isinstance(hashed, str)

        assert verify_password(password, hashed)

        with pytest.raises(HTTPException):
            verify_password("WrongPassword", hashed)


class TestJWTHandler:
    def test_access_token_creation_and_verification(self):
        payload = {
            "sub": "123",
            "email": "test@example.com",
            "role": "user"
        }

        token = create_access_token(payload)
        assert token is not None
        assert isinstance(token, str)

        decoded = verify_token(token, token_type="access")
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@example.com"
        assert decoded["role"] == "user"
        assert decoded["type"] == "access"

    def test_refresh_token_creation_and_verification(self):
        payload = {
            "sub": "456",
            "email": "refresh@example.com",
            "role": "admin"
        }

        token = create_refresh_token(payload)
        assert token is not None

        decoded = verify_token(token, token_type="refresh")
        assert decoded["sub"] == "456"
        assert decoded["email"] == "refresh@example.com"
        assert decoded["type"] == "refresh"

    def test_token_type_validation(self):
        payload = {"sub": "123", "email": "test@example.com"}

        access_token = create_access_token(payload)

        with pytest.raises(HTTPException):
            verify_token(access_token, token_type="refresh")

    def test_token_purpose_validation(self):
        payload = {"sub": "123", "email": "test@example.com"}

        reset_token = create_password_reset_token(payload)

        decoded = verify_token(reset_token, token_purpose="password_reset", token_type="reset")
        assert decoded["purpose"] == "password_reset"
        assert decoded["type"] == "reset"

        with pytest.raises(HTTPException):
            verify_token(reset_token, token_purpose="email_verification")

    def test_invalid_token_verification(self):
        with pytest.raises(HTTPException):
            verify_token("invalid.token.here")

        fake_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.fake_signature"
        with pytest.raises(HTTPException):
            verify_token(fake_token)


class TestEmailValidation:
    def test_email_domain_validation(self):
        valid_emails = [
            "user@gruposese.com",
            "test@volkswagen.com.br",
            "admin@gruposese.com"
        ]

        for email in valid_emails:
            validate_email_domain(email)

        invalid_emails = [
            "user@10minutemail.com",
            "test@temp-mail.org",
            "spam@guerrillamail.com",
            "user@gmail.com",
            "test@hotmail.com"
        ]

        for email in invalid_emails:
            with pytest.raises(HTTPException) as exc_info:
                validate_email_domain(email)
            assert "O e-mail deve ser do domínio" in str(exc_info.value.detail)

