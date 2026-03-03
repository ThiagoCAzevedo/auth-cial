from sqlalchemy.orm import sessionmaker
from database.engine import engine


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        raise
    finally:
        db.close()
