import unittest
from tihan.sdv.securetransfer.rsa_utils import encrypt_message, decrypt_message,generate_private_key,generate_public_key

class TestRSAUtils(unittest.TestCase):

    def setUp(self):
        self.private_key = generate_private_key()
        self.public_key = generate_public_key(self.private_key)
        with open(self.private_key, "r") as f:
            self.private_key = f.read()
        with open(self.public_key, "r") as f:
            self.public_key = f.read()
        self.message = "This is a test message."

    def test_encrypt_decrypt(self):
        encrypted_message = encrypt_message(self.message, self.public_key)
        decrypted_message = decrypt_message(encrypted_message, self.private_key)
        if isinstance(decrypted_message, bytes):
            decrypted_message = decrypted_message.decode()
        self.assertEqual(self.message, decrypted_message)

    def test_encrypt_with_invalid_key(self):
        with self.assertRaises(ValueError):
            decrypt_message(b"invalid_encrypted_message", "invalid_key")

if __name__ == "__main__":
    unittest.main()