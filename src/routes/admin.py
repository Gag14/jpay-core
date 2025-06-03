from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.enums.network_type import NetworkType

from src.models.enums import transaction_status
from src.repositories.coin_repository import CoinRepository
from src.repositories.merchant_repository import MerchantRepository
from src.repositories.wallet_repository import WalletRepository
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.balance_repository import BalanceRepository
from src.db.session import get_db

router = APIRouter()
merchant_Repository = MerchantRepository()
wallet_Repository = WalletRepository()
transaction_Repository = TransactionRepository()
transaction_status = transaction_status.TransactionStatus
balance_Repository = BalanceRepository()
coin_Repository = CoinRepository()
network_type = NetworkType
@router.post("/coins/test-create")

def test_create_coin(db: Session = Depends(get_db)):
    coin_data = {
        "name": "Tether USD",
        "symbol": "USDT",
        "network": network_type.TRON,  # Pass enum value
        "contract_address": "T1234567890",
        "decimals": 6,
        "is_active": True
    }
    return coin_Repository.create(db, coin_data)

@router.get("/coins")
def get_coins(db: Session = Depends(get_db)):
    return coin_Repository.get_all(db)
@router.post("/merchants/test-create")
def test_create_merchant(db: Session = Depends(get_db)):
    merchant_data = {
        "name": "TestMerchant",
        "contact_email": "test@example.com",
        "api_key_hashed": "hashed_api_key_123",
        "is_active": True,
        "webhook_url": "https://example.com/webhook"
    }
    created = merchant_Repository.create(db, merchant_data)
    return {"created_merchant_id": created.id}


@router.get("/merchants/test-get/{merchant_id}")
def test_get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    merchant = merchant_Repository.get_by_id(db, merchant_id)
    if merchant:
        return {
            "name": merchant.name,
            "email": merchant.contact_email,
            "webhook": merchant.webhook_url
        }
    return {"error": "Merchant not found"}

@router.post("/wallets/test-create")
def test_create_wallet(db: Session = Depends(get_db)):
    wallet_data = {
        "merchant_id": 1,
        "address": "TRXabc12345",
        "private_key": "private_key_here",
        "coin": "USDT",
        "network": "TRON"
    }
    wallet = wallet_Repository.create(db, wallet_data)
    return {"wallet_id": wallet.id}

@router.post("/transactions/test-create")
def test_create_transaction(db: Session = Depends(get_db)):
    transaction_data = {
        "merchant_id": 1,
        "wallet_id": 1,
        "tx_type": "deposit",
        "tx_hash": "0xABC123456789",
        "amount": 100.50,
        "coin": "USDT",
        "network": "TRON",
        "status": transaction_status.PENDING
    }
    tx = transaction_Repository.create(db, transaction_data)
    return {"transaction_id": tx.id}

@router.post("/balances/test-create")
def test_create_balance(db: Session = Depends(get_db)):
    balance_data = {
        
        "merchant_id": 1,
        "coin_symbol": "USDT2",
        "network": "TRON5",
        "balance": 0,
        "wallet_id": 1,
        "coin_id": 4
    }
    created = balance_Repository.create(db, balance_data)
    return {"created_balance_id": created.id}