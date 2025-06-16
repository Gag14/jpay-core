from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime, timedelta

from src.core.celery.tasks.transaction_monitor import monitor_pending_transactions
from src.db.session import get_db
from src.schemas.deposit import DepositRequest, DepositResponse
from src.core.dependencies.auth import get_current_merchant
from src.services.wallet_service import WalletService
from src.repositories.coin_repository import CoinRepository
from src.repositories.fiat_repository import FiatCurrencyRepository
from src.utils.rates import get_crypto_to_fiat_rate  # We'll mock this
from src.repositories.transaction_repository import TransactionRepository
from src.models.enums.transaction_status import TransactionStatus

router = APIRouter()
coin_repo = CoinRepository()
wallet_service = WalletService()
tx_repo = TransactionRepository()
fiat_repo = FiatCurrencyRepository()

@router.post("/request", response_model=DepositResponse)
def create_deposit_request(
    data: DepositRequest,
    db: Session = Depends(get_db),
    merchant = Depends(get_current_merchant)
):
    # Validate fiat currency
    fiat = fiat_repo.get_by_code(db, data.fiat_currency)
    if not fiat or not fiat.is_active:
        raise HTTPException(status_code=400, detail="Unsupported or inactive fiat currency")

    # Validate coin
    coins = coin_repo.get_active_coins(db)
    coins = coin_repo.get_active_coins(db)
    for coin in coins:
        print({
        "symbol": coin.symbol,
        "network": coin.network,
        "contract": coin.contract_address
    })
    coin = coin_repo.get_by_symbol_and_network(db, data.crypto_coin, data.network)
    print(data.crypto_coin, data.network)
    if not coin or not coin.is_active:
        raise HTTPException(status_code=400, detail="Unsupported crypto coin or network")

    # Get live rate
    rate = get_crypto_to_fiat_rate(data.crypto_coin, data.fiat_currency)
    if not rate:
        raise HTTPException(status_code=502, detail="Unable to retrieve crypto rate")

    # Convert fiat → expected crypto amount
    expected_crypto_amount = Decimal(data.fiat_amount) / Decimal(rate)
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    # Create a deposit wallet for this request
    deposit_wallet = wallet_service.create_wallet(
        db=db,
        owner_type="SYSTEM",
        merchant_id=merchant.id,
        coin=data.crypto_coin,
        network=data.network
    )

    transaction = tx_repo.create(db, {
        "merchant_id": merchant.id,
        "wallet_id": deposit_wallet.id,
        "tx_type": "deposit",
        "tx_hash": deposit_wallet.address,  # No hash yet, pending deposit
        "amount": expected_crypto_amount,
        "coin": coin.symbol,
        "network": coin.network.value if hasattr(coin.network, "value") else coin.network,
        "status": TransactionStatus.PENDING,
        "fiat_amount": data.fiat_amount,
        "fiat_currency_code": data.fiat_currency,
        "created_at": datetime.utcnow()
    })

    return DepositResponse(
        transaction_id=transaction.id,
        deposit_address=deposit_wallet.address,
        expected_crypto_amount=round(expected_crypto_amount, 6),
        rate=rate,
        expires_at=expires_at
    )


@router.get("/trigger-monitor")
def trigger_monitor():
    monitor_pending_transactions.delay()
    return {"status": "monitoring triggered"}
