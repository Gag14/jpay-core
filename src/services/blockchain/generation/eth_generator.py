from eth_account import Account
import secrets
from src.services.blockchain.generation.base_generator import WalletGenerator

class EthWalletGenerator(WalletGenerator):

    def generate_address(self):
        # Generate a random private key
        private_key = "0x" + secrets.token_hex(32)
        # Create an account object
        acct = Account.from_key(private_key)
        # Return address and private key
        print(f"Generated Ethereum address: {acct.address} with private key: {private_key}")
        return acct.address, private_key 
    
             
        
