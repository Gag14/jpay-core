import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, UniqueConstraint, Enum
from src.db.base import Base
from src.models.enums.transaction_status import TransactionStatus
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    tx_type = Column(String(10), nullable=False)  # "deposit" / "withdraw"
    tx_hash = Column(String(3000), unique=True)
    amount = Column(Numeric(36, 8), nullable=False)
    coin = Column(String(20), nullable=False)
    network = Column(String(20), nullable=False)
    status = Column(Enum(TransactionStatus, native_enum=True), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    fiat_currency_code = Column(String(3), ForeignKey("fiat_currencies.code"))
    fiat_amount = Column(Numeric(precision=18, scale=2), nullable=True)

    fiat_currency = relationship("FiatCurrency", lazy="joined")
    wallet = relationship("Wallet", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")


from src.models import fiat_currency, merchant, wallet
