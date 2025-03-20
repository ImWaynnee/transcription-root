from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    print("Database initialized with tables:", inspector.get_table_names())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 