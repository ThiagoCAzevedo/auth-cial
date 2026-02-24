from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from dotenv import load_dotenv
from helpers.http_exceptions import HTTP_Exceptions
import jwt, os


load_dotenv("config/.env")


class JWTHandler:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_days: int = 1):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )

    @staticmethod
    def verify_token(token: str, token_purpose: str = None, token_type: str = None) -> dict:
        try:
            decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
            
            if token_type and decoded.get("type") != token_type:
                raise HTTP_Exceptions.http_401(f"Invalid token type. Expected: {token_type}.")
            
            if token_purpose and decoded.get("purpose") != token_purpose:
                raise HTTP_Exceptions.http_401("Invalid token purpose.")
            
            return decoded

        except jwt.ExpiredSignatureError:
            raise HTTP_Exceptions.http_401("Token expired.")

        except jwt.InvalidTokenError:
            raise HTTP_Exceptions.http_401("Invalid token.")
        
    @staticmethod
    def create_password_reset_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

        to_encode.update({
            "exp": expire,
            "purpose": "password_reset",
            "type": "reset"
        })

        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )