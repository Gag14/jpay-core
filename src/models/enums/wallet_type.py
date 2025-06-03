import enum
from sqlalchemy import Enum

class WalletType(enum.Enum):
    MERCHANT = "Merchant"
    SYSTEM = "System"
    PLATFORM = "Platform"
