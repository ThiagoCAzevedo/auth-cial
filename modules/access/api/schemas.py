from pydantic import BaseModel, EmailStr, validator
from common.services.validators import validate_email_domain, validate_password


class EmailSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ChangePasswordSchema(BaseModel):
    password: str

    @validator("password")
    def check_password(cls, value):
        validate_password(value)
        return value


class ResetPasswordSchema(BaseModel):
    password: str

    @validator("password")
    def check_password(cls, value):
        validate_password(value)
        return value


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: bool
    is_verified: bool

    class Config:
        from_attributes = True


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    remember_me: bool
    user: UserResponseSchema

    class Config:
        from_attributes = True


class RefreshTokenResponseSchema(BaseModel):
    refresh_token: str

