import asyncio
from celery import shared_task
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.repositories.transaction_repository import TransactionRepository
from src.services.blockchain.services import get_blockchain_service
from src.core.callbacks.sender import send_callback
from src.services.blockchain.transfer.transfer_service import TransferService
from src.repositories.wallet_repository import WalletRepository

transaction_repo = TransactionRepository()
wallet_repo = WalletRepository()
transfer_service = TransferService()

@shared_task
def monitor_pending_transactions():
    db: Session = SessionLocal()
    try:
        print("[DEBUG] Starting transaction monitoring...")

        
        pending_txns = transaction_repo.get_pending_transactions(db)
        print(f"[DEBUG] Found {len(pending_txns)} pending transactions")

        for txn in pending_txns:
            print(f"[DEBUG] Checking transaction: {txn.id} on address {txn.wallet.address}")

            blockchain_service = get_blockchain_service(txn.coin, txn.network)
            confirmed, tx_hash = blockchain_service.check_transaction_status(txn.wallet.address, float(txn.amount))
            print(f"[DEBUG] Service Result: {txn.amount}, with hash {tx_hash} on confirmed {confirmed}")

            if confirmed:
                # Update transaction as confirmed
                transaction_repo.mark_as_confirmed(db, txn.id, tx_hash)

                # Transfer to merchant's main wallet
                transfer_service.transfer_to_main_wallet(db, txn.id)

                # Send callback to merchant
                asyncio.run(send_callback(txn))
    finally:
        db.close()
