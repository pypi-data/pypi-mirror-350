import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def generate_aes_key(key_size=256):
    """Generate a random AES key."""
    return get_random_bytes(key_size // 8)

def encrypt_data(data, key):
    """Encrypt data using AES encryption."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv, ct_bytes

def decrypt_data(iv, ct, key):
    """Decrypt data using AES encryption."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

