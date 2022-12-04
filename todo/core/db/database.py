from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DB_ENGINE, DB_ENGINES, POSTGRES_DATABASE_URI, SQLITE_DATABASE_URI

if DB_ENGINE == DB_ENGINES.SQLITE:
    engine = create_engine(SQLITE_DATABASE_URI, connect_args={'check_same_thread': False})
else:
    engine = create_engine(POSTGRES_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
