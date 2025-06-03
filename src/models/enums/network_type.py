import enum
from sqlalchemy import Enum

class NetworkType(enum.Enum):
    TRON = "TRON"
    BITCOIN = "BITCOIN"
    ETHEREUM = "ETHEREUM"
