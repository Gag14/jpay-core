from src.repositories.coin_repository import CoinRepository
from src.models.enums.wallet_type import WalletType
from src.models.wallet import Wallet
from src.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from src.models.enums.wallet_type import WalletType, wallet_type_db
from src.models.wallet import Wallet
from sqlalchemy.exc import NoResultFound
from src.services.blockchain.generation import get_wallet_generator

class WalletRepository(BaseRepository[Wallet]):
    def __init__(self):
        super().__init__(Wallet)
        self.coin_repo = CoinRepository()
    def get_main_wallet(self, db: Session, merchant_id: int, coin: str, network: str):
        return db.query(Wallet).filter_by(
            merchant_id=merchant_id,
            coin=coin,
            network=network,
            is_main=True,
            is_active=True
        ).first()
        
        
        
    def create_main_wallet(self, db: Session, merchant_id: int, address: str, private_key: str, coin: str, network: str) -> Wallet:
        # Set all existing wallets for this merchant/coin/network as not main
        db.query(Wallet).filter_by(
            merchant_id=merchant_id,
            coin=coin,
            network=network,
            is_main=True
        ).update({"is_main": False})

        new_wallet = Wallet(
            owner_type=WalletType.MERCHANT,
            merchant_id=merchant_id,
            address=address,
            private_key=private_key,
            coin=coin,
            network=network,
            is_active=True,
            is_main=True
        )

        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)
        return new_wallet
    
    
    
    def get_platform_wallet(self, db: Session, coin: str, network: str) -> Wallet:
        return db.query(Wallet).filter(
            Wallet.owner_type == WalletType.PLATFORM.name,
            Wallet.coin == coin,
            Wallet.network == network,
            Wallet.is_active == True
        ).first()



    def create_platform_wallet(
        self,
        db: Session,
        coin: str,
        network: str,
    ) -> Wallet:
        
        wallet_generator = get_wallet_generator(coin, network)
        if not wallet_generator:
            raise ValueError(f"No wallet generator found for coin {coin} on network {network}")


        address, private_key = wallet_generator.generate_address()
        coin_obj = self.coin_repo.get_by_symbol_and_network(db, symbol=coin, network=network)
        if not coin_obj:
            raise ValueError(f"Coin {coin} on network {network} does not exist in the system")

        new_wallet_data = {
            "address": address,
            "private_key": private_key,
            "coin": coin.upper(),
            "network": network.upper(),
            "is_active": True,
            "owner_type": WalletType.PLATFORM,
            "merchant_id": 10,  # Platform wallet does not belong to a merchant
            "is_main": False  # Platform wallet is not a main wallet
        }

        return self.create(db, new_wallet_data)
