from fastapi import Request, Depends, HTTPException
from src.models.merchant import Merchant

def get_current_merchant(request: Request) -> Merchant:
    merchant = getattr(request.state, "merchant", None)
    if merchant is None:
        raise HTTPException(status_code=401, detail="Unauthorized: no merchant found in request")
    return merchant
