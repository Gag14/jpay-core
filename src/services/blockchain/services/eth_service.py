from tronpy import Tron
from tronpy.keys import PrivateKey
from src.services.blockchain.services.base_service import BlockchainService

class EthService(BlockchainService):
    def __init__(self):
        self.client = Tron(network="nile")

    def check_transaction_status(self, address: str, expected_amount: float):
        
        return False, None

    def transfer(self, from_address, to_address, private_key, amount):
        
        return 123456789
