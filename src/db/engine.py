from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://myuser:Test123456@localhost:5432/mydb"

engine = create_engine(
    DATABASE_URL,
    echo_pool=True,
    pool_size=10,
    max_overflow=0,
    pool_timeout=3,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
