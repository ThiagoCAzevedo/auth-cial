from pydantic import BaseModel, EmailStr, validator
from common.services.validators import validate_email_domain, validate_password


class UpdateUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    status: bool | None = None
    is_verified: bool | None = None
    refresh_token: str | None = None

    @validator("email")
    def check_email(cls, value):
        if value:
            validate_email_domain(value)
        return value

    @validator("password")
    def check_password(cls, value):
        if value:
            validate_password(value)
        return value

