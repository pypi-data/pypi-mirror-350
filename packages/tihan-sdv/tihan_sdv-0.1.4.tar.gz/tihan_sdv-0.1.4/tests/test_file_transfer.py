import unittest
import os
import tempfile
from pathlib import Path
from unittest import mock
import pytest
from tihan.sdv.securetransfer.file_transfer import  FileSender, FileReceiver
from tihan.sdv.securetransfer.aes_utils import generate_aes_key, encrypt_data, decrypt_data
from tihan.sdv.securetransfer.rsa_utils import generate_private_key, generate_public_key, encrypt_message, decrypt_message
import zipfile

class TestFileTransfer(unittest.TestCase):

    def setUp(self):
        # Generate RSA key pair for testing
        self.private_key_file = generate_private_key()
        self.public_key_file = generate_public_key(self.private_key_file)
        with open(self.private_key_file, 'r') as pkf:
            self.private_key = pkf.read()
        with open(self.public_key_file, 'r') as pubkf:
            self.public_key = pubkf.read()
        # Generate AES key for testing
        self.aes_key = generate_aes_key()
        # self.file_transfer = FileTransfer(self.public_key, self.private_key)

    def test_aes_encryption_decryption(self):
        original_data = b"This is a test message."
        iv, encrypted_data = encrypt_data(original_data, self.aes_key)
        decrypted_data = decrypt_data(iv, encrypted_data, self.aes_key)
        self.assertEqual(original_data, decrypted_data)

    def test_rsa_encryption_decryption(self):
        message = "This is a secret message."
        encrypted_message = encrypt_message(message.encode('utf-8'), self.public_key)
        decrypted_message = decrypt_message(encrypted_message, self.private_key).decode('utf-8')
        self.assertEqual(message, decrypted_message)

    def test_file_transfer_process(self):
        private_key_file = generate_private_key()
        public_key_file = generate_public_key(private_key_file)
        with open(private_key_file, "r") as f:
            private_key = f.read()
        with open(public_key_file, "r") as f:
            public_key = f.read()
        sender = FileSender(public_key)
        receiver = FileReceiver(private_key)
        original_file_content = b"This is the content of the file."
        file_path = self.get_temp_file(original_file_content)
        encrypted_file_path = file_path + ".enc"
        encrypted_key_path = file_path + ".key.enc"
        decrypted_file_path = file_path + ".dec"
        encrypted_path, aes_key = sender.encrypt_file(file_path, encrypted_file_path)
        sender.encrypt_key(aes_key, encrypted_key_path)
        aes_key_dec = receiver.decrypt_key(encrypted_key_path)
        receiver.decrypt_file(encrypted_file_path, aes_key_dec, decrypted_file_path)
        with open(decrypted_file_path, "rb") as f:
            decrypted_content = f.read()
        self.assertEqual(original_file_content, decrypted_content)
        os.remove(file_path)
        os.remove(decrypted_file_path)
        os.remove(encrypted_file_path)
        os.remove(encrypted_key_path)
        os.remove(private_key_file)
        os.remove(public_key_file)

    def get_temp_file(self, content=b"test data"):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'wb') as f:
            f.write(content)
        return path

    def test_encrypt_and_decrypt_file(self):
        private_key_file = generate_private_key()
        public_key_file = generate_public_key(private_key_file)
        with open(private_key_file, "r") as f:
            private_key = f.read()
        with open(public_key_file, "r") as f:
            public_key = f.read()
        sender = FileSender(public_key)
        receiver = FileReceiver(private_key)
        original_content = b"super secret data"
        temp_file = self.get_temp_file(original_content)
        enc_file = temp_file + ".enc"
        dec_file = temp_file + ".dec"
        encrypted_path, aes_key = sender.encrypt_file(temp_file, enc_file)
        self.assertTrue(Path(encrypted_path).exists())
        self.assertIn(len(aes_key), (16, 24, 32))
        decrypted_path = receiver.decrypt_file(encrypted_path, aes_key, dec_file)
        with open(decrypted_path, "rb") as f:
            decrypted = f.read()
        self.assertEqual(decrypted, original_content)
        os.remove(temp_file)
        os.remove(enc_file)
        os.remove(dec_file)
        os.remove(private_key_file)
        os.remove(public_key_file)

    def test_encrypt_and_decrypt_key(self):
        private_key_file = generate_private_key()
        public_key_file = generate_public_key(private_key_file)
        with open(private_key_file, "r") as f:
            private_key = f.read()
        with open(public_key_file, "r") as f:
            public_key = f.read()
        sender = FileSender(public_key)
        receiver = FileReceiver(private_key)
        aes_key = os.urandom(16)
        enc_key_path = tempfile.mktemp()
        encrypted_key_path = sender.encrypt_key(aes_key, enc_key_path)
        self.assertTrue(Path(encrypted_key_path).exists())
        decrypted_key = receiver.decrypt_key(encrypted_key_path)
        self.assertEqual(decrypted_key, aes_key)
        os.remove(enc_key_path)
        os.remove(private_key_file)
        os.remove(public_key_file)

    def test_zip_package(self):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        sender = FileSender(public_key)
        file1 = self.get_temp_file(b"file1")
        file2 = self.get_temp_file(b"file2")
        zip_path = tempfile.mktemp(suffix=".zip")
        zip_file = sender.zip_package([file1, file2], zip_path)
        self.assertTrue(Path(zip_file).exists())
        with zipfile.ZipFile(zip_file, 'r') as zf:
            self.assertEqual(set(zf.namelist()), {Path(file1).name, Path(file2).name})
        os.remove(file1)
        os.remove(file2)
        os.remove(zip_path)

    @mock.patch("boto3.client")
    def test_upload_to_s3_mock(self, mock_boto):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        sender = FileSender(public_key)
        file_path = self.get_temp_file(b"s3data")
        mock_s3 = mock.Mock()
        mock_boto.return_value = mock_s3
        sender.upload_to_s3(file_path, "bucket", "key")
        mock_s3.upload_file.assert_called_once()
        os.remove(file_path)

    @mock.patch("subprocess.run")
    def test_send_file_scp_mock(self, mock_run):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        sender = FileSender(public_key)
        file_path = self.get_temp_file(b"scpdata")
        # Only count the scp call
        def side_effect(*args, **kwargs):
            if "scp" in args[0][0]:
                return mock.DEFAULT
            else:
                # Simulate successful keygen
                return None
        mock_run.side_effect = side_effect
        sender.send_file_scp(file_path, "user", "1.2.3.4", "/tmp/remote")
        # Check that at least one call was for scp
        scp_calls = [call for call in mock_run.call_args_list if "scp" in call[0][0][0]]
        self.assertTrue(len(scp_calls) == 1)
        os.remove(file_path)

if __name__ == "__main__":
    unittest.main()