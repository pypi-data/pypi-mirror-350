import subprocess
import os

def generate_private_key(key_size=2048):
    private_key_file = "private_key.pem"
    subprocess.run(["openssl", "genrsa", "-out", private_key_file, str(key_size)])
    return private_key_file

def generate_public_key(private_key_file):
    public_key_file = "public_key.pem"
    subprocess.run(["openssl", "rsa", "-pubout", "-in", private_key_file, "-out", public_key_file])
    return public_key_file

def encrypt_message(message, public_key):
    if isinstance(message, bytes):
        with open("temp_message.txt", "wb") as message_file:
            message_file.write(message)
    else:
        with open("temp_message.txt", "w") as message_file:
            message_file.write(message)
    with open("temp_pubkey.pem", "wb") as pubkey_file:
        pubkey_file.write(public_key)
    subprocess.run([
        "openssl", "rsautl", "-encrypt", "-inkey", "temp_pubkey.pem",
        "-pubin", "-in", "temp_message.txt", "-out", "encrypted_message.bin"
    ])
    with open("encrypted_message.bin", "rb") as enc_file:
        encrypted_message = enc_file.read()
    os.remove("temp_message.txt")
    os.remove("temp_pubkey.pem")
    os.remove("encrypted_message.bin")
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    with open("temp_encrypted.bin", "wb") as enc_file:
        enc_file.write(encrypted_message)
    with open("temp_private_key.pem", "wb") as privkey_file:
        privkey_file.write(private_key)
    result = subprocess.run([
        "openssl", "rsautl", "-decrypt", "-inkey", "temp_private_key.pem",
        "-in", "temp_encrypted.bin", "-out", "decrypted_message.txt"
    ])
    if result.returncode != 0 or not os.path.exists("decrypted_message.txt"):
        raise ValueError("Decryption failed")
    with open("decrypted_message.txt", "rb") as dec_file:
        decrypted_message = dec_file.read()
    os.remove("temp_encrypted.bin")
    os.remove("temp_private_key.pem")
    os.remove("decrypted_message.txt")
    return decrypted_message