# Configuration settings for the encryption project

# File paths
BASE_DIR = "encryption-project/src"
KEYS_DIR = f"{BASE_DIR}/keys"
CERTS_DIR = f"{BASE_DIR}/certificates"
TEST_FILES_DIR = f"{BASE_DIR}/test_files"

# Key sizes
RSA_KEY_SIZE = 2048
AES_KEY_SIZE = 32  # 256 bits

# Other constants
ENCRYPTED_FILE_SUFFIX = ".enc"
DECRYPTED_FILE_SUFFIX = ".dec"
ENCRYPTED_FILE_PATH = f"encrypted_file{ENCRYPTED_FILE_SUFFIX}"
ENCRYPTED_KEY_PATH = "encrypted_key.bin"