# from cryptography.fernet import Fernet
# import hashlib
# import uuid

# fernet_key = Fernet.generate_key()  # Store securely per app instance
# fernet = Fernet(fernet_key)


import hashlib
from cryptography.fernet import Fernet
from src.core.config import settings
import secrets

fernet = Fernet(settings.FERNET_SECRET)

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

def generate_raw_api_key() -> str:
    return secrets.token_urlsafe(32)  # Strong, URL-safe key

def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode()).decode()
