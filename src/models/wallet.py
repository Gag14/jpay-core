import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.db.base import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    address = Column(String(100), nullable=False, unique=True)
    private_key = Column(String(255), nullable=False)
    coin = Column(String(20), nullable=False)
    network = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    balances = relationship("Balance", back_populates="wallet", uselist=False, cascade="all, delete-orphan")
    merchant = relationship("Merchant", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")
