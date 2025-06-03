from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.merchant import MerchantRegisterRequest, MerchantRegisterResponse
from src.services.merchant_service import MerchantService
from sqlalchemy import text
import time


router = APIRouter()
merchant_service = MerchantService()


@router.post("/register", response_model=MerchantRegisterResponse)
def register_merchant(data: MerchantRegisterRequest, db: Session = Depends(get_db)):
    raw_key = merchant_service.register_merchant(db, data.name, data.contact_email)
    return {"api_key": raw_key}
