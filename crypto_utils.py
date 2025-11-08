from cryptography.fernet import Fernet
import os
import base64
import hashlib

def get_encryption_key():
    """Get or generate encryption key from environment"""
    key = os.environ.get("SESSION_SECRET")
    if not key:
        raise ValueError("SESSION_SECRET environment variable not set")
    
    key_bytes = hashlib.sha256(key.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)

def encrypt_cookie(cookie_value: str) -> str:
    """Encrypt Instagram session cookie"""
    if not cookie_value:
        return ""
    
    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(cookie_value.encode())
    return encrypted.decode()

def decrypt_cookie(encrypted_value: str) -> str:
    """Decrypt Instagram session cookie"""
    if not encrypted_value:
        return ""
    
    f = Fernet(get_encryption_key())
    decrypted = f.decrypt(encrypted_value.encode())
    return decrypted.decode()
