from sqlalchemy.orm import Session
from typing import Optional
from src.repositories.base_repository import BaseRepository
from src.models.fiat_currency import FiatCurrency  # Adjust import path if needed

class FiatCurrencyRepository(BaseRepository[FiatCurrency]):
    def __init__(self):
        super().__init__(FiatCurrency)

    def get_by_code(self, db: Session, code: str) -> Optional[FiatCurrency]:
        return db.query(FiatCurrency).filter(FiatCurrency.code == code.upper()).first()

    def get_active(self, db: Session) -> list[FiatCurrency]:
        return db.query(FiatCurrency).filter(FiatCurrency.is_active == True).all()
