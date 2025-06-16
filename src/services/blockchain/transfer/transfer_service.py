from src.repositories.coin_repository import CoinRepository
from src.repositories.balance_repository import BalanceRepository
from src.services.blockchain.generation import get_wallet_generator
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.wallet_repository import WalletRepository
from src.services.blockchain import get_blockchain_service
from src.repositories.merchant_repository import MerchantRepository
from src.services.blockchain.commission.commission_service import CommissionService
from datetime import datetime
from sqlalchemy.orm import Session


class TransferService:
    def __init__(self):
        self.tx_repo = TransactionRepository()
        self.wallet_repo = WalletRepository()
        self.balance_repo = BalanceRepository()
        self.coin_repo = CoinRepository()  
        self.commission_service = CommissionService(MerchantRepository(), self.wallet_repo)
    def transfer_to_main_wallet(self, db: Session, tx_id: int) -> str:
        # Load transaction
        tx = self.tx_repo.get_by_id(db, tx_id)
        if not tx:
            raise ValueError(f"Transaction {tx_id} not found")
        if not tx.wallet or not tx.wallet.address:
            raise ValueError("Transaction wallet missing or invalid")

        from_wallet_id = tx.wallet_id
        from_wallet = self.wallet_repo.get_by_id(db=db, id=from_wallet_id)  
        merchant_id = tx.merchant_id
        coin = tx.coin
        network = tx.network
        amount = tx.amount
        private_key = from_wallet.private_key

        try:
            self.commission_service.apply_commission(db, tx)
        except Exception as e:
            print(f"[ERROR] Commission application failed: {e}")
            raise ValueError(f"Failed to apply commission: {e}")
        # Get or create main wallet
        main_wallet = self.wallet_repo.get_main_wallet(db, merchant_id, coin, network)
        if not main_wallet:
            generator = get_wallet_generator(coin, network)

        # 2. Generate address + private key
            address, private_key_m = generator.generate_address()
            main_wallet = self.wallet_repo.create_main_wallet(db=db, merchant_id=merchant_id, address=address, private_key=private_key_m, coin=coin, network=network)
            print(f"[DEBUG] Created new main wallet: {main_wallet.address} for merchant {merchant_id}")

        # Ensure main wallet is active
        if not main_wallet.is_active:
            raise ValueError(f"Main wallet {main_wallet.address} is not active")

        # Check if transfer amount is valid
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero")

        # Log transfer attempt
        print(f"[DEBUG] Initiating transfer of {amount} from {from_wallet.address} to {main_wallet.address}")
        # Call chain-specific transfer logic
        blockchain_service = get_blockchain_service(coin, network)
        txid = blockchain_service.transfer(
            from_address=from_wallet.address,
            to_address=main_wallet.address,
            private_key=private_key,
            amount=amount
        )
# inside transfer_to_main_wallet()
        coin_obj = self.coin_repo.get_by_symbol_and_network(db, symbol=coin, network=network)
        if not coin_obj:
            raise ValueError(f"Coin {coin} on {network} not found")
        balance = self.balance_repo.get_by_merchant_coin_network(db, merchant_id, coin, network)

        if balance:
            self.balance_repo.update_balance(db, balance, amount)
        else:
            self.balance_repo.create_balance(db, {
                "merchant_id": merchant_id,
                "coin_symbol": coin,
                "network": network,
                "balance": amount,
                "wallet_id": main_wallet.id,
                "coin_id": coin_obj.id
            })

        # Update transaction hash (optional)
        self.tx_repo.update_tx_hash(db, tx_id, txid)
        return txid
