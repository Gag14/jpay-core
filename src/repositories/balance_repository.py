from src.models.balance import Balance
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository
from typing import Optional

class BalanceRepository(BaseRepository[Balance]):
    def __init__(self):
        super().__init__(Balance)

    def get_by_merchant_coin_network(self, db: Session, merchant_id: int, coin_symbol: str, network: str) -> Optional[Balance]:
        return db.query(Balance).filter_by(
            merchant_id=merchant_id,
            coin_symbol=coin_symbol,
            network=network
        ).first()

    def update_balance(self, db: Session, balance_obj: Balance, amount_delta: float) -> Balance:
        balance_obj.balance += amount_delta
        db.commit()
        db.refresh(balance_obj)
        return balance_obj

    def create_balance(self, db: Session, data: dict) -> Balance:
        return self.create(db, data)