from sqlalchemy.orm import Session
from typing import Optional, List
from src.repositories.base_repository import BaseRepository
from src.models.coin import Coin
from src.models.enums.network_type import NetworkType
class CoinRepository(BaseRepository[Coin]):
    def __init__(self):
        super().__init__(Coin)

    def get_by_symbol_and_network(self, db: Session, symbol: str, network: NetworkType) -> Optional[Coin]:
        return db.query(Coin).filter(
            Coin.symbol == symbol.upper(),
            Coin.network == network
        ).first()

    def get_active_coins(self, db: Session) -> List[Coin]:
        return db.query(Coin).filter(Coin.is_active == True).all()