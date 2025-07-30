import os
import subprocess
import zipfile
from pathlib import Path
from typing import Union,IO

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

from tihan.sdv.securetransfer.aes_utils import generate_aes_key, encrypt_data, decrypt_data
from tihan.sdv.securetransfer.rsa_utils import encrypt_message, decrypt_message
from tihan.sdv.securetransfer.config import ENCRYPTED_FILE_PATH, ENCRYPTED_KEY_PATH

class FileSender:
    """
    A utility class to encrypt files using AES symmetric encryption and RSA asymmetric
    encryption for key exchange. Also supports sending files over a socket, zipping, and uploading
    to an S3 bucket.
    """

    def __init__(self, receiver_public_key: bytes):
        self.receiver_public_key = receiver_public_key  

    def encrypt_file(self,
                     filepath: Union[str, Path],
                     output_path: Union[str, Path] = ENCRYPTED_FILE_PATH) -> tuple[Path, bytes]:
        """
        Encrypts the file at `filepath` with a newly generated AES key,
        writes the encrypted content to `output_path`, and returns the AES key.
        """
        filepath = Path(filepath)
        output_path = Path(output_path)

        # Generate a fresh AES key
        aes_key = generate_aes_key()

        # Read plaintext data
        with filepath.open('rb') as f:
            data = f.read()

        # Encrypt data (correct argument order)
        iv, encrypted_data = encrypt_data(data, aes_key)

        # Write iv + encrypted data to disk
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('wb') as f:
            f.write(iv + encrypted_data)

        return output_path, aes_key

    def encrypt_key(self,
                    aes_key: bytes,
                    output_path: Union[str, Path] = ENCRYPTED_KEY_PATH) -> Path:
        """
        Encrypts the AES key with the receiver's RSA public key and writes
        the encrypted key to disk at `output_path`.
        """
        output_path = Path(output_path)

        # Encrypt AES key using RSA
        encrypted_key = encrypt_message(aes_key, self.receiver_public_key)

        # Write encrypted key
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('wb') as f:
            f.write(encrypted_key)

        return output_path

    def send_file_scp(self,
                      local_path: Union[str, Path],
                      remote_user: str,
                      remote_ip: str,
                      remote_path: Union[str, Path]) -> None:
        local_path = Path(local_path)
        remote_path = str(remote_path)
        command = [
            "scp",
            str(local_path),
            f"{remote_user}@{remote_ip}:{remote_path}"
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"SCP file transfer failed: {e}")

    def zip_package(self,
                    files: list[Union[str, Path]],
                    output_zip: Union[str, Path]) -> Path:
        """
        Creates a ZIP archive containing the provided list of file paths.
        """
        output_zip = Path(output_zip)
        output_zip.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                file = Path(file)
                zf.write(file, arcname=file.name)

        return output_zip

    # def upload_to_s3(self,
    #                  file_path: Union[str, Path],
    #                  bucket_name: str,
    #                  object_key: str) -> None:
    #     """
    #     Uploads `file_path` to the specified S3 `bucket_name` under `object_key`.
    #     """
    #     file_path = Path(file_path)
    #     s3 = boto3.client('s3')
    #     try:
    #         s3.upload_file(str(file_path), bucket_name, object_key)
    #     except (BotoCoreError, ClientError) as e:
    #         raise RuntimeError(f"Failed to upload to S3: {e}")


    def upload_to_s3(
            self,
            file_path:Union[str,Path], 
            bucket_name:str, 
            object_name:str=None,
            minio_endpoint:str='localhost:9000', 
            access_key:str='minioadmin', 
            secret_key:str='minioadmin', 
            use_ssl:bool=False):
        """
        Uploads a file to a MinIO bucket using boto3.

        Args:
            file_path (str): Local path to the file to be uploaded.
            bucket_name (str): Name of the bucket to upload to.
            object_name (str): Name of the object in MinIO (optional).
            minio_endpoint (str): Endpoint of the MinIO server.
            access_key (str): Access key for MinIO.
            secret_key (str): Secret key for MinIO.
            use_ssl (bool): Whether to use HTTPS (True) or HTTP (False).
        """
        if object_name is None:
            object_name = file_path.split("/")[-1]

        # Create the client
        s3_client = boto3.client(
            's3',
            endpoint_url=f"http{'s' if use_ssl else ''}://{minio_endpoint}",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4'),
            region_name='in'
        )

        # Ensure the bucket exists (optional, can be removed if not needed)
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except s3_client.exceptions.clientError as e:
            if e.response['Error']['Code'] =='400':
                # Bucket Does not exist ;trying to create
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                raise RuntimeError(f"Bucket check failed:{e}")

        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to bucket '{bucket_name}' as '{object_name}'")


class FileReceiver:
    def __init__(self,own_private_key: bytes):
        self.own_private_key = own_private_key

    def decrypt_key(self,
                    encrypted_key_path: Union[str, Path]) -> IO :
        """
        Reads and decrypts the AES key from `encrypted_key_path` using
        the user's RSA private key.
        """
        encrypted_key_path = Path(encrypted_key_path)
        with encrypted_key_path.open('rb') as f:
            encrypted_key = f.read()

        aes_key = decrypt_message(encrypted_key, self.own_private_key)
        with open("aes-key-decrypted.dec",'wb') as f:
            f.write(aes_key)
        return f

    def decrypt_file(self,
                     encrypted_file_path: Union[str, Path],
                     aes_key: bytes,
                     output_path: Union[str, Path]) -> Path:
        """
        Decrypts the file at `encrypted_file_path` using the provided `aes_key`
        and writes the plaintext to `output_path`.
        """
        encrypted_file_path = Path(encrypted_file_path)
        output_path = Path(output_path)

        with encrypted_file_path.open('rb') as f:
            file_data = f.read()
        iv = file_data[:16]
        encrypted_data = file_data[16:]
        plaintext = decrypt_data(iv, encrypted_data, aes_key)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('wb') as f:
            f.write(plaintext)

        return output_path


