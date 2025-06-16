from typing import Optional
from datetime import datetime

from sqlalchemy import Enum
from src.models.wallet import Wallet
from src.models.enums.wallet_type import WalletType
from src.repositories.wallet_repository import WalletRepository
from src.services.blockchain.generation import get_wallet_generator


class WalletService:
    def __init__(self):
        self.wallet_repo = WalletRepository()

    def create_wallet(
        self,
        db,
        owner_type: WalletType,
        merchant_id: int,
        coin: str,
        network: str
    ) -> Wallet:
        # 1. Get correct generator
        generator = get_wallet_generator(coin, network)

        # 2. Generate address + private key
        address, private_key = generator.generate_address()
        print(f"Generated address: {address}, private key: {private_key}")
        # 3. Prepare wallet data
        wallet_data = {
            "owner_type": owner_type.value if hasattr(owner_type, "value") else owner_type,
            "merchant_id": merchant_id,
            "coin": coin,
            "network": network.value if hasattr(network, "value") else network,
            "address": address,
            "private_key": private_key,
            "is_active": True,
            "created_at": datetime.utcnow()
        }

        # 4. Save using repository
        return self.wallet_repo.create(db, wallet_data)

    def get_wallet_by_id(self, db, wallet_id: int) -> Optional[Wallet]:
        return self.wallet_repo.get_by_id(db, wallet_id)

    def get_wallet_by_address(self, db, address: str) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.address == address).first()

    def get_merchant_main_wallet(self, db, merchant_id: int, coin: str, network: str) -> Optional[Wallet]:
        return db.query(Wallet).filter(
            Wallet.merchant_id == merchant_id,
            Wallet.wallet_role == WalletType.main,
            Wallet.coin == coin,
            Wallet.network == network
        ).first()

    def get_or_create_reserve_wallet(self, db, merchant_id: int, coin: str, network: str) -> Wallet:
        existing = db.query(Wallet).filter(
            Wallet.merchant_id == merchant_id,
            Wallet.wallet_role == WalletType.reserve,
            Wallet.coin == coin,
            Wallet.network == network
        ).first()

        if existing:
            return existing

        return self.create_wallet(
            db=db,
            owner_type="merchant",
            merchant_id=merchant_id,
            wallet_role=WalletType.reserve,
            coin=coin,
            network=network
        )
