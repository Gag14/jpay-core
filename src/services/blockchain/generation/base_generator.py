from abc import ABC, abstractmethod
from typing import Tuple

class WalletGenerator(ABC):
    @abstractmethod
    def generate_address(self) -> Tuple[str, str]:
        """
        Returns a tuple of (address, private_key)
        """
        pass
