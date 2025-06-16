from src.services.blockchain.generation.tron_generator import TronWalletGenerator
from src.services.blockchain.generation.eth_generator import EthWalletGenerator
from src.services.blockchain.generation.btc_generator import BtcWalletGenerator
# Add more generators as needed

def get_wallet_generator(coin: str, network: str):
    if coin.upper() == "USDT" or coin.upper() == "TRX" and network.upper() == "TRON":
        return TronWalletGenerator()
    elif network.value.upper() == "ETHEREUM":
        return EthWalletGenerator()
    elif network.value.upper() == "BITCOIN":
        return BtcWalletGenerator()
    raise NotImplementedError(f"Wallet generation not supported for {coin} on {network}")
