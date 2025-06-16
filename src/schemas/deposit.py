from pydantic import BaseModel, condecimal, Field
from decimal import Decimal
from datetime import datetime
from src.models.enums.network_type import NetworkType


PositiveFiat = condecimal(gt=0, decimal_places=2)

class DepositRequest(BaseModel):
    fiat_amount: Decimal = Field(..., gt=0, decimal_places=2)

    fiat_currency: str  # e.g. 'EUR'
    crypto_coin: str    # e.g. 'TRX'
    network: NetworkType

# src/schemas/deposit.py
class DepositResponse(BaseModel):
    transaction_id: int
    deposit_address: str
    expected_crypto_amount: Decimal
    rate: Decimal
    expires_at: datetime
