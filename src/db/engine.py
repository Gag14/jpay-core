from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings  # adjust the import path accordingly


engine = create_engine(
    settings.DATABASE_URL,
    echo_pool=True,
    pool_size=10,
    max_overflow=0,
    pool_timeout=3,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
