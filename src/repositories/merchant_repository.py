from sqlalchemy.orm import Session
from src.db.base import Base
from src.models.merchant import Merchant
from src.repositories.base_repository import BaseRepository


class MerchantRepository(BaseRepository[Merchant]):
    def __init__(self):
        super().__init__(Merchant)

    def get_by_api_key(self, db: Session, api_key_hashed: str) -> Merchant | None:
        return db.query(self.model).filter(self.model.api_key_hashed == api_key_hashed).first()

    def get_active_merchants(self, db: Session):
        return db.query(self.model).filter(self.model.is_active == True).all()
