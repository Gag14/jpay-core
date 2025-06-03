from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from src.db.base import Base
from src.models.enums.network_type import NetworkType


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False, unique=True)
    network = Column(Enum(NetworkType), nullable=False)
    contract_address = Column(String(100), nullable=True)
    decimals = Column(Integer, nullable=False, default=6)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    balances = relationship("Balance", back_populates="coin", cascade="all, delete-orphan")
