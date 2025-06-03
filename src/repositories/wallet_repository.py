from src.models.wallet import Wallet
from src.repositories.base_repository import BaseRepository

class WalletRepository(BaseRepository[Wallet]):
    def __init__(self):
        super().__init__(Wallet)
