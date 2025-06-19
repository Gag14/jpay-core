from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.models.enums.transaction_status import TransactionStatus
from src.models.enums.tx_type import TransactionType

from pydantic import BaseModel
from datetime import datetime
from typing import List
from src.models.enums.transaction_status import TransactionStatus
from src.models.enums.tx_type import TransactionType

class TransactionOut(BaseModel):
    id: int
    merchant_id: int
    wallet_id: int
    tx_type: TransactionType
    tx_hash: Optional[str] = None
    amount: float
    status: TransactionStatus
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionListResponse(BaseModel):
    total: int
    items: List[TransactionOut]



class TransactionFilterRequest(BaseModel):
    merchant_ids: List[int]
    status: Optional[TransactionStatus] = None
    tx_type: Optional[TransactionType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0
