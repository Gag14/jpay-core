from src.services.blockchain.services.tron_service import TronService
from src.services.blockchain.services.eth_service import EthService
from src.services.blockchain.services.btc_service import BtcService

def get_blockchain_service(coin: str, network: str):
    if coin.upper() in ["USDT", "TRX"] and network.upper() == "TRON":
        return TronService()
    elif network.upper() == "ETHEREUM":
        return EthService()
    elif network.upper() == "BITCOIN":
        return BtcService()
    raise NotImplementedError(f"No blockchain service for {coin} on {network}")
