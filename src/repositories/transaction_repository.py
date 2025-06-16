from datetime import datetime
from src.models.enums.transaction_status import TransactionStatus
from src.models.transaction import Transaction
from src.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)
        
        
    def update_tx_hash(self, db: Session, transaction_id: int, tx_hash: str):
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if tx:
            tx.tx_hash = tx_hash
            db.commit()
            db.refresh(tx)
        return tx

    def get_pending_transactions(self, db: Session):
        return db.query(Transaction).filter(Transaction.status == TransactionStatus.PENDING).all()

    def mark_as_confirmed(self, db: Session, transaction_id: int, tx_hash: str):
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        print(f"[DEBUG] confirmed Transaction {tx.id}:")
        
        if tx:
            tx.tx_hash = tx_hash
            tx.status = TransactionStatus.SUCCESS
            tx.confirmed_at = datetime.utcnow()
            db.commit()
            db.refresh(tx)
        return tx
