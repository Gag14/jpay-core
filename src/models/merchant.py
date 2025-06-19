import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Numeric, String, Boolean, DateTime
from src.db.base import Base
from src.models.wallet import Wallet
class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=True)
    api_key_hashed = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    webhook_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    commission_rate = Column(Numeric(5, 4), default=0.00)  
    
    wallets = relationship("Wallet", back_populates="merchant", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="merchant", cascade="all, delete-orphan")
