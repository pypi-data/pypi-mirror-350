import os
import tempfile
from pathlib import Path
import pytest
from unittest import mock
from tihan.sdv.securetransfer.file_transfer import FileSender, FileReceiver
from tihan.sdv.securetransfer.aes_utils import generate_aes_key, encrypt_data, decrypt_data
from tihan.sdv.securetransfer.rsa_utils import generate_private_key, generate_public_key, encrypt_message, decrypt_message
import zipfile

@pytest.fixture
def rsa_keypair(tmp_path):
    private_key_file = generate_private_key()
    public_key_file = generate_public_key(private_key_file)
    with open(private_key_file, 'rb') as pkf:
        private_key = pkf.read()
    with open(public_key_file, 'rb') as pubkf:
        public_key = pubkf.read()
    yield private_key, public_key, private_key_file, public_key_file
    os.remove(private_key_file)
    os.remove(public_key_file)

@pytest.fixture
def aes_key():
    return generate_aes_key()

@pytest.fixture
def temp_file(tmp_path):
    def _make_temp_file(content=b"test data"):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'wb') as f:
            f.write(content)
        return path
    return _make_temp_file

def test_aes_encryption_decryption(aes_key):
    original_data = b"This is a test message."
    iv, encrypted_data = encrypt_data(original_data, aes_key)
    decrypted_data = decrypt_data(iv, encrypted_data, aes_key)
    assert original_data == decrypted_data

def test_rsa_encryption_decryption(rsa_keypair):
    private_key, public_key, *_ = rsa_keypair
    message = "This is a secret message."
    encrypted_message = encrypt_message(message.encode('utf-8'), public_key)
    decrypted_message = decrypt_message(encrypted_message, private_key).decode('utf-8')
    assert message == decrypted_message

def test_file_transfer_process(rsa_keypair, temp_file):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    receiver = FileReceiver(private_key)
    original_file_content = b"This is the content of the file."
    file_path = temp_file(original_file_content)
    encrypted_file_path = file_path + ".enc"
    encrypted_key_path = file_path + ".key.enc"
    decrypted_file_path = file_path + ".dec"
    encrypted_path, aes_key = sender.encrypt_file(file_path, encrypted_file_path)
    sender.encrypt_key(aes_key, encrypted_key_path)
    with open(encrypted_key_path, 'rb') as f:
        pass  # just to ensure file exists
    aes_key_dec = receiver.decrypt_key(encrypted_key_path)
    receiver.decrypt_file(encrypted_file_path, aes_key_dec, decrypted_file_path)
    with open(decrypted_file_path, "rb") as f:
        decrypted_content = f.read()
    assert original_file_content == decrypted_content
    for p in [file_path, decrypted_file_path, encrypted_file_path, encrypted_key_path]:
        os.remove(p)

def test_encrypt_and_decrypt_file(rsa_keypair, temp_file):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    receiver = FileReceiver(private_key)
    original_content = b"super secret data"
    tempf = temp_file(original_content)
    enc_file = tempf + ".enc"
    dec_file = tempf + ".dec"
    encrypted_path, aes_key = sender.encrypt_file(tempf, enc_file)
    assert Path(encrypted_path).exists()
    assert len(aes_key) in (16, 24, 32)
    decrypted_path = receiver.decrypt_file(encrypted_path, aes_key, dec_file)
    with open(decrypted_path, "rb") as f:
        decrypted = f.read()
    assert decrypted == original_content
    for p in [tempf, enc_file, dec_file]:
        os.remove(p)

def test_encrypt_and_decrypt_key(rsa_keypair):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    receiver = FileReceiver(private_key)
    aes_key = os.urandom(16)
    enc_key_path = tempfile.mktemp()
    encrypted_key_path = sender.encrypt_key(aes_key, enc_key_path)
    assert Path(encrypted_key_path).exists()
    decrypted_key = receiver.decrypt_key(encrypted_key_path)
    assert decrypted_key == aes_key
    os.remove(enc_key_path)

def test_zip_package(rsa_keypair, temp_file):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    file1 = temp_file(b"file1")
    file2 = temp_file(b"file2")
    zip_path = tempfile.mktemp(suffix=".zip")
    zip_file = sender.zip_package([file1, file2], zip_path)
    assert Path(zip_file).exists()
    with zipfile.ZipFile(zip_file, 'r') as zf:
        assert set(zf.namelist()) == {Path(file1).name, Path(file2).name}
    for p in [file1, file2, zip_path]:
        os.remove(p)

@mock.patch("boto3.client")
def test_upload_to_s3_mock(mock_boto, rsa_keypair, temp_file):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    file_path = temp_file(b"s3data")
    mock_s3 = mock.Mock()
    mock_boto.return_value = mock_s3
    sender.upload_to_s3(file_path, "bucket", "key")
    mock_s3.upload_file.assert_called_once()
    os.remove(file_path)

@mock.patch("subprocess.run")
def test_send_file_scp_mock(mock_run, rsa_keypair, temp_file):
    private_key, public_key, *_ = rsa_keypair
    sender = FileSender(public_key)
    file_path = temp_file(b"scpdata")
    mock_run.return_value = mock.DEFAULT
    sender.send_file_scp(file_path, "user", "1.2.3.4", "/tmp/remote")
    scp_calls = [call for call in mock_run.call_args_list if "scp" in call[0][0][0]]
    assert len(scp_calls) == 1
    os.remove(file_path)
