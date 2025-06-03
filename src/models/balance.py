import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, UniqueConstraint
from src.db.base import Base

class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    coin_symbol = Column(String(20), nullable=False)  # e.g., "TRX", "USDT", "ETH"
    network = Column(String(20), nullable=False)  # e.g., "TRON", "ETH", "BTC"
    balance = Column(Numeric(36, 8), default=0)  # accurate up to 10^-8
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    coin_id = Column(Integer, ForeignKey("coins.id"), nullable=False)
    coin = relationship("Coin", back_populates="balances")
    wallet = relationship("Wallet", back_populates="balances")

    __table_args__ = (
        UniqueConstraint('merchant_id', 'coin_symbol', 'network', name='unique_balance_per_coin'),
    )
