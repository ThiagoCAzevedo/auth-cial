from sqlalchemy import create_engine
from config.settings import settings


engine = create_engine(
    f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PSWD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}",
    pool_pre_ping=True,
    pool_recycle=3600,
)
