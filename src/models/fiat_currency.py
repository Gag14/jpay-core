from sqlalchemy import Column, String, Boolean
from src.db.base import Base


class FiatCurrency(Base):
    __tablename__ = "fiat_currencies"

    code = Column(String(3), primary_key=True)  # e.g. 'EUR'
    name = Column(String(50))  # e.g. 'Euro'
    symbol = Column(String(5))  # e.g. '€'
    is_active = Column(Boolean, default=True)
