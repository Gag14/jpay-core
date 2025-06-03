from src.models.balance import Balance
from src.repositories.base_repository import BaseRepository

class BalanceRepository(BaseRepository[Balance]):
    def __init__(self):
        super().__init__(Balance)
