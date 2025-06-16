from abc import ABC, abstractmethod

class BlockchainService(ABC):
    @abstractmethod
    def check_transaction_status(self, address: str, expected_amount: float) -> tuple[bool, str | None]:
        pass

    @abstractmethod
    def transfer(self, from_address: str, to_address: str, private_key: str, amount: float) -> str:
        pass
