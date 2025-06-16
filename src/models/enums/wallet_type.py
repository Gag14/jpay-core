import enum
from sqlalchemy import Enum as SqlEnum

class WalletType(enum.Enum):
    MERCHANT = "Merchant"
    SYSTEM = "System"
    PLATFORM = "Platform"
    RESERVE = "Reserve"

wallet_type_db = SqlEnum(WalletType, name="wallet_type_enum")
