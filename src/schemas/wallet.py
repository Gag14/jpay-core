from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime

class WalletCreateResponse(BaseModel):
    main_wallet_address: str
    reserve_wallet_address: str


class WalletOut(BaseModel):
    id: int
    merchant_id: int
    address: str
    coin: str
    network: str
    is_main: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class WalletsResponse(BaseModel):
    items: List[WalletOut]
