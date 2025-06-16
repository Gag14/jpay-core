import httpx
from src.models.transaction import Transaction

async def send_callback(transaction: Transaction):
    callback_url = transaction.merchant.webhook_url
    if not callback_url:
        print("No callback URL provided for transaction.")
        return
    payload = {
        "transaction_id": transaction.id,
        "status": transaction.status.value,
        "amount": float(transaction.amount),
        "coin": transaction.coin,
        "network": transaction.network,
        "tx_hash": transaction.tx_hash,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(callback_url, json=payload, timeout=10)
            response.raise_for_status()
        except Exception as e:
            # Optional: add retry logic, logging, or push to failed queue
            print(f"Callback failed: {e}")
