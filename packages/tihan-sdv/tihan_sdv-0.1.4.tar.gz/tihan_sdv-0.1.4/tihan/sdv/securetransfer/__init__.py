# This file is intentionally left blank.


"""
    Agenda: This module helps to demonstrate secure file transfer with the help of certificate authority,
    with the implementation of the Encryption and Decryption Function.

    Demonstration of Security with the help of a hybrid of RSA and AES Algorithm.

    Workflow: The workflow involves three processes:
        1. Generation of AES key.
        2. Securing the AES key with RSA algorithm implemented in the CA (Public key of receiver) and providing an encrypted AES key.
        3. Encrypting the file with the non-secured AES key using AES algorithm.
        4. Sending the encrypted file along with the encrypted key.
        5. Key can only be decrypted with the help of receiver's private key.
        6. Once the key is decrypted, it will help in decrypting the file.
"""
