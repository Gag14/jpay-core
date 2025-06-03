from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.merchant import MerchantRegisterRequest, MerchantRegisterResponse
from src.services.merchant_service import MerchantService
from sqlalchemy import text
import time


router = APIRouter()
merchant_service = MerchantService()
@router.get("/test")
def core_test():
    return {"message": "Core route working!"}


@router.get("/simulate-db-pool")
def simulate_db_pool(db: Session = Depends(get_db)):
    time.sleep(2)  # Simulate slow DB usage
    db.execute(text("SELECT 1"))  # ✅ wrap in text()
    return {"message": "DB connection used"}

@router.post("/register", response_model=MerchantRegisterResponse)
def register_merchant(data: MerchantRegisterRequest, db: Session = Depends(get_db)):
    raw_key = merchant_service.register_merchant(db, data.name, data.contact_email)
    return {"api_key": raw_key}
