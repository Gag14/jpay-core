from sqlalchemy.orm import Session
from src.models.admin_user import AdminUser
from src.repositories.base_repository import BaseRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminUserRepository(BaseRepository[AdminUser]):
    def __init__(self):
        super().__init__(AdminUser)

    def get_by_username(self, db: Session, username: str) -> AdminUser | None:
        return db.query(AdminUser).filter(AdminUser.username == username).first()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
