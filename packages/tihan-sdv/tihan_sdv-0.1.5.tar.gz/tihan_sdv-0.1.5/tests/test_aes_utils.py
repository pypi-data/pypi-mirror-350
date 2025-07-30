import pytest
from tihan.sdv.securetransfer.aes_utils import generate_aes_key, encrypt_data, decrypt_data

def test_generate_aes_key():
    key = generate_aes_key()
    assert len(key) == 32  # AES-256 key size

def test_encrypt_decrypt_data():
    key = generate_aes_key()
    original_data = b"This is a secret message."
    iv, ct = encrypt_data(original_data, key)
    decrypted_data = decrypt_data(iv, ct, key)
    assert decrypted_data == original_data

def test_encrypt_decrypt_data_invalid_key():
    key = generate_aes_key()
    original_data = b"This is a secret message."
    iv, ct = encrypt_data(original_data, key)
    wrong_key = generate_aes_key()
    with pytest.raises(ValueError):
        decrypt_data(iv, ct, wrong_key)

def test_encrypt_empty_data():
    key = generate_aes_key()
    original_data = b""
    iv, ct = encrypt_data(original_data, key)
    decrypted_data = decrypt_data(iv, ct, key)
    assert decrypted_data == original_data

def test_encrypt_decrypt_multiple_messages():
    key = generate_aes_key()
    messages = [b"msg1", b"another message", b"1234567890", b"!@#$%^&*()"]
    for msg in messages:
        iv, ct = encrypt_data(msg, key)
        decrypted = decrypt_data(iv, ct, key)
        assert decrypted == msg

def test_decrypt_with_wrong_iv():
    key = generate_aes_key()
    original_data = b"Secret"
    iv, ct = encrypt_data(original_data, key)
    wrong_iv = generate_aes_key()[:16]
    with pytest.raises(ValueError):
        decrypt_data(wrong_iv, ct, key)
    iv2,cv2 = encrypt_data(original_data, key)
    
    # Use a different key for decryption
    wrong_key = generate_aes_key()
    with pytest.raises(ValueError):
        decrypt_data(iv2,cv2, wrong_key)