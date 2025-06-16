import os
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from src.services.blockchain.generation.base_generator import WalletGenerator

class BtcWalletGenerator(WalletGenerator):
    def generate_address(self):
        # Step 1: Generate a random 32-byte private key
        private_key = os.urandom(32)

        # Step 2: Derive the public key using ecdsa (secp256k1)
        sk = SigningKey.from_string(private_key, curve=SECP256k1)
        vk = sk.verifying_key
        public_key = b'\x04' + vk.to_string()

        # Step 3: SHA-256 hash of the public key
        sha256_pk = hashlib.sha256(public_key).digest()

        # Step 4: RIPEMD-160 hash of the SHA-256
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_pk)
        hashed_pk = ripemd160.digest()

        # Step 5: Add version byte (0x00 for mainnet)
        versioned_pk = b'\x00' + hashed_pk

        # Step 6: Double SHA-256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_pk).digest()).digest()[:4]

        # Step 7: Append checksum
        binary_address = versioned_pk + checksum

        # Step 8: Base58 encoding
        address = base58.b58encode(binary_address).decode()

        return address, private_key.hex()

    # Example usage:
    # print(generate_btc_address())