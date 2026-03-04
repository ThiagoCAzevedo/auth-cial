from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # APP CONFIG
    APP_NAME: str
    APP_URL: str    
    FILES_DRIVER: str

    APP_VERIFY_EMAIL: str
    APP_RESET_PASSWORD: str

    # MYSQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PSWD: str
    MYSQL_DATABASE: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PSWD: str

    class Config:
        env_file = "config/.env"
        extra = "forbid"
        case_sensitive = True


settings = Settings()