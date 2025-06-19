from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.admin.dependencies.admin_permissions import get_allowed_merchant_ids
from src.repositories.merchant_repository import MerchantRepository
from src.admin.jwtauth import create_access_token
from src.db.session import get_db

router = APIRouter()


@router.get("/merchants")
def list_merchants(
    db: Session = Depends(get_db),
    merchant_ids: list[int] | None = Depends(get_allowed_merchant_ids)
):
    return MerchantRepository().get_all(get_db())