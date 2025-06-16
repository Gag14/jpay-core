from sqlalchemy.orm import Session
from src.repositories.merchant_repository import MerchantRepository
from src.utils.security import hash_api_key, generate_raw_api_key, encrypt_api_key, decrypt_api_key
import secrets

class MerchantService:
    def __init__(self):
        self.repo = MerchantRepository()

    def register_merchant(self, db: Session, name: str, email: str) -> str:
        # Generate API key
        raw_key = generate_raw_api_key()
        hashed_key = hash_api_key(raw_key)
        encrypted_key = encrypt_api_key(raw_key)
        # Save to DB
        self.repo.create(db, {
            "name": name,
            "contact_email": email,
            "api_key_hashed": hashed_key
        })

        # Return raw key (only once!)
        return encrypted_key

    def get_by_api_key(self, db: Session, raw_key: str):
        # decrypted_key = decrypt_api_key(raw_key)
        hashed_key = hash_api_key(raw_key)
        return self.repo.get_by_api_key(db, hashed_key)
