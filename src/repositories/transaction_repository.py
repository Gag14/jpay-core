from src.models.transaction import Transaction
from src.repositories.base_repository import BaseRepository

class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)
