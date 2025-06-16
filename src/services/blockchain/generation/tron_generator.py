from tronpy import Tron
from src.services.blockchain.generation.base_generator import WalletGenerator

class TronWalletGenerator(WalletGenerator):
    def generate_address(self):
        client = Tron()
        wallet = client.generate_address()
        return wallet['base58check_address'], wallet['private_key']
