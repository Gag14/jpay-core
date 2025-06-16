from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FERNET_SECRET: str
    DATABASE_URL: str  

    class Config:
        env_file = ".env"

settings = Settings()
