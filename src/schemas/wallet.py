from pydantic import BaseModel
from enum import Enum

class WalletCreateResponse(BaseModel):
    main_wallet_address: str
    reserve_wallet_address: str
