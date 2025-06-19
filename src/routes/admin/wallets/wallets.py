from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.admin.dependencies.admin_permissions import get_allowed_merchant_ids
from src.models.wallet import Wallet
from src.schemas.wallet import WalletsResponse

router = APIRouter()

@router.get("/main", response_model=WalletsResponse)
def get_main_wallets(
    db: Session = Depends(get_db),
    allowed_ids: list[int] | None = Depends(get_allowed_merchant_ids)
):
    if allowed_ids is not None and not allowed_ids:
        return {"items": []}

    query = db.query(Wallet).filter(Wallet.is_main.is_(True))
    if allowed_ids is not None:
        query = query.filter(Wallet.merchant_id.in_(allowed_ids))

    wallets = query.order_by(Wallet.created_at.desc()).all()
    return {"items": wallets}
