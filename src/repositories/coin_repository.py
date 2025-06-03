from src.repositories.base_repository import BaseRepository
from src.models.coin import Coin  # Adjust the path to where your Coin model is defined

class CoinRepository(BaseRepository[Coin]):
    def __init__(self):
        super().__init__(Coin)
