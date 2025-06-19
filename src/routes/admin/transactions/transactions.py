from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from src.db.session import get_db
from src.admin.dependencies.admin_permissions import get_allowed_merchant_ids
from src.models.transaction import Transaction
from src.schemas.transaction_filter import TransactionFilterRequest,TransactionListResponse, TransactionOut
from fastapi import HTTPException, Path

router = APIRouter()

@router.get("/by-merchants", response_model=TransactionListResponse)
def get_transactions_by_merchants(
    payload: TransactionFilterRequest,
    db: Session = Depends(get_db),
    allowed_ids: list[int] | None = Depends(get_allowed_merchant_ids),
):
    if allowed_ids is not None:
        filtered_ids = [mid for mid in payload.merchant_ids if mid in allowed_ids]
    else:
        filtered_ids = payload.merchant_ids

    if not filtered_ids:
        return {"total": 0, "items": []}

    base_query = db.query(Transaction).filter(Transaction.merchant_id.in_(filtered_ids))

    if payload.status:
        base_query = base_query.filter(Transaction.status == payload.status)
    if payload.tx_type:
        base_query = base_query.filter(Transaction.tx_type == payload.tx_type)
    if payload.start_date:
        base_query = base_query.filter(Transaction.created_at >= payload.start_date)
    if payload.end_date:
        base_query = base_query.filter(Transaction.created_at <= payload.end_date)

    total = base_query.with_entities(func.count()).scalar()

    results = (
        base_query.order_by(Transaction.created_at.desc())
        .offset(payload.offset)
        .limit(payload.limit)
        .all()
    )

    return {"total": total, "items": results}


@router.get("/{tx_id}", response_model=TransactionOut)
def get_transaction_by_id(
    tx_id: int = Path(..., description="Transaction ID"),
    db: Session = Depends(get_db),
    allowed_ids: list[int] | None = Depends(get_allowed_merchant_ids),
):
    transaction = db.query(Transaction).filter(Transaction.id == tx_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Enforce merchant permission
    if allowed_ids is not None and transaction.merchant_id not in allowed_ids:
        raise HTTPException(status_code=403, detail="Permission denied for this merchant")

    return transaction
