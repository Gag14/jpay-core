from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.services.wallet_service import WalletService
from src.schemas.wallet import WalletCreateRequest, WalletCreateResponse
from src.repositories.coin_repository import CoinRepository
from src.models.enums.wallet_type import WalletType
from src.core.dependencies.auth import get_current_merchant

router = APIRouter()
wallet_service = WalletService()
coin_repo = CoinRepository()



@router.post("/", response_model=WalletCreateResponse)
def create_wallet(
    data: WalletCreateRequest,
    db: Session = Depends(get_db),
    merchant=Depends(get_current_merchant)
):
    coin = coin_repo.get_by_symbol_and_network(db, data.coin, data.network)
    if not coin or not coin.is_active:
        raise HTTPException(status_code=400, detail="Coin or network is invalid or inactive")
    try:
        role_enum = WalletType(data.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid wallet role")
    
    
    wallet = wallet_service.create_wallet(
        db=db,
        owner_type="merchant",
        merchant_id=merchant.id,
        coin=data.coin,
        network=data.network
    )

    return WalletCreateResponse(
        address=wallet.address,
        coin=wallet.coin,
        network=wallet.network,
        role=wallet.wallet_role.value
    )