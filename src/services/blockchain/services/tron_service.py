from tronpy import Tron
from tronpy.keys import PrivateKey
from src.services.blockchain.services.base_service import BlockchainService

class TronService(BlockchainService):
    def __init__(self):
        self.client = Tron(network="nile")

    def check_transaction_status(self, address: str, expected_amount: float):
        # Placeholder: In production you'd scan recent transactions to that address
        try:
            txs = self.client.get_account_balance(address)
            print(f"[DEBUG] Transaction {txs}, {expected_amount * 1_000_000}")
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch transactions for address {address}: {e}")
            return False, None
        if not txs:
            print(f"[DEBUG] No transactions found for address {address}")
            return False, None
        # for tx in txs:
        #     if float(tx['value']) >= expected_amount:
        #         return True, tx['txID']
        if txs >= expected_amount:  # Convert TRX to SUN
            print(f"[DEBUG] Transaction found for address {address} with sufficient amount")
            return True, txs
        return False, None

    def transfer(self, from_address, to_address, private_key, amount):
        priv = PrivateKey(bytes.fromhex(private_key))
        txn = (
            self.client.trx.transfer(from_address, to_address, int(amount * 1_000_000))
            .build()
            .sign(priv)
            .broadcast()
        )
        return txn['txid']
