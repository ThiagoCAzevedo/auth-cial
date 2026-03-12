from pydantic import BaseModel, EmailStr, validator
from common.services.validators import validate_email_domain, validate_password


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @validator("email")
    def check_email(cls, value):
        validate_email_domain(value)
        return value

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


class RegisterResponseSchema(BaseModel):
    message: str
    user: UserResponseSchema

    class Config:
        from_attributes = True

