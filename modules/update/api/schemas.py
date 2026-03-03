from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from common.services.validators import UserValidators


class EmailSchema(BaseModel):
    email: EmailStr


class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = None

    @field_validator("email")
    def validate_email_domain(cls, value):
        if value:
            UserValidators.validate_email_domain(value)
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        if value:
            UserValidators.validate_password(value)
        return value


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    remember_me: bool
    token_type: str
    user: dict


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: bool
    role: Optional[str]

    class Config:
        from_attributes = True
