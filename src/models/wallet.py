import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, Boolean
from src.db.base import Base
from src.models.enums.wallet_type import WalletType, wallet_type_db

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    owner_type = Column(wallet_type_db, nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    address = Column(String(100), nullable=False, unique=True)
    private_key = Column(String(255), nullable=False)
    coin = Column(String(20), nullable=False)
    network = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_main = Column(Boolean, default=False)  # Add this line
    
    balances = relationship("Balance", back_populates="wallet", uselist=False, cascade="all, delete-orphan")
    merchant = relationship("Merchant", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")


from src.models.balance import Balance
