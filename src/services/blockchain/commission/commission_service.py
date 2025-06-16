from decimal import Decimal
from sqlalchemy.orm import Session
from src.models.transaction import Transaction
from src.repositories.merchant_repository import MerchantRepository
from src.repositories.wallet_repository import WalletRepository
from src.services.blockchain import get_blockchain_service

class CommissionService:
    def __init__(self, merchant_repo: MerchantRepository, wallet_repo: WalletRepository):
        self.merchant_repo = merchant_repo
        self.wallet_repo = wallet_repo

    def apply_commission(self, db: Session, tx: Transaction) -> str:
        merchant_id = tx.merchant_id
        coin = tx.coin
        network = tx.network
        amount = tx.amount
        from_wallet = tx.wallet
        private_key = from_wallet.private_key

        if amount <= 0:
            raise ValueError("Invalid transaction amount")

        # Get commission rate (default to 2%)
        merchant = self.merchant_repo.get_by_id(db, merchant_id)
        rate = Decimal(merchant.commission_rate or "0.02")
        commission_amount = amount * rate

        # Get platform wallet
        platform_wallet = self.wallet_repo.get_platform_wallet(db, coin, network)
        if not platform_wallet:
            platform_wallet = self.wallet_repo.create_platform_wallet(db=db, coin=coin, network=network)

        # Transfer commission
        blockchain_service = get_blockchain_service(coin, network)
        txid = blockchain_service.transfer(
            from_address=from_wallet.address,
            to_address=platform_wallet.address,
            private_key=private_key,
            amount=commission_amount
        )

        # Optionally: log commission, update platform balance here

        return txid
