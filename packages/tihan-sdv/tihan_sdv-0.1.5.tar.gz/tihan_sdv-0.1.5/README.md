# TiHAN SDV

**TiHAN SDV** (Software Defined Vehicle) is a modular Python framework for simulating, visualizing, and experimenting with autonomous vehicle technologies. This module helps in providing tools for secure file-transfer, compression, and advanced sensor visualization.

---

## 🚗 Features

- **Encryption Module**: Certificate Authority (CA) management, file/message encryption & decryption using OpenSSL.
- **Compression Module**: (Pluggable, see source for details.)
- **Visualizer Module**:
  - **Ultrasonic Sensor Visualization**: Real-time, animated display of multi-sensor data.
  - **Parking Assist Visualization**: Camera-based parking overlay, trajectory lines, and car position rendering.
- **Extensible**: Easily add new sensors, visualizations, or algorithms.
- **Tested**: Includes automated tests for core modules.

---

## 📦 Installation
```sh
pip install tihan-sdv
```

#### or

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/tihan_sdv.git
   cd tihan_sdv
   ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Install as a package:(Optional-- as the package is already pushed in pypi)**

    ```sh
    pip install .
    ```
---

## 🚀 Quick Start

Ultrasonic Visualizer Example

```python
from tihan.sdv.visualizer.ultrasonic import UltrasonicVisualizer
import random

visualizer = UltrasonicVisualizer(
    distance_1=76, distance_2=25, distance_3=35,
    distance_4=random.randint(10, 50), distance_5=random.randint(10, 50),
    distance_6=random.randint(10, 50), distance_7=random.randint(10, 50),
    distance_8=random.randint(10, 50), distance_9=random.randint(10, 50),
    distance_10=random.randint(10, 50), distance_11=random.randint(10, 50),
    distance_12=random.randint(10, 50)
)

# Update with new data
new_data = {f'distance_{i+1}': random.randint(10, 100) for i in range(12)}
visualizer.set_distances(new_data)
```
---

## Parking Assist Visualizer
Run the parking assist visualizer:

> 📌**Note :**
> Requires a webcam and calibration data.


## 🛡️ Securetransfer Module 
Demonstrates secure file transfer using a hybrid approach that combines RSA and AES encryption algorithms. The goal is to provide a modular and extensible framework for encrypting files, managing certificates, and ensuring secure communication.
### Securetransfer Module Structure
The project is organized into the following directories and files:

- **securetransfer/**: Contains the main source code for the project.
  - **ca.py**: Implements the `CertificateAuthority` class for managing certificates.
  - **aes_utils.py**: Provides utility functions for AES encryption and decryption.
  - **rsa_utils.py**: Contains utility functions for RSA encryption and decryption.
  - **file_transfer.py**: Manages the workflow for secure file transfer.
  - **config.py**: Holds configuration settings and constants.

### Securetransfer Usage
- To generate certificates, use the `CertificateAuthority` class in `ca.py`.
- For AES encryption and decryption, utilize the functions in `aes_utils.py`.
- For RSA operations, refer to the functions in `rsa_utils.py`.
- The `file_transfer.py` module integrates these utilities to facilitate secure file transfers.

## Securetransfer Example
### Sender Side 
```python

from tihan.sdv.securetransfer.file_transfer import FileSender
from pathlib import Path

# Load the receiver's public key (as bytes)
with open(r"public_key.pem", "rb") as f:
    receiver_public_key = f.read()

# Initialize FileSender
sender = FileSender(receiver_public_key)

# Path to the file you want to send
file_to_send = "demo.txt"

# Step 1: Encrypt the file
encrypted_file_path, aes_key = sender.encrypt_file(file_to_send)

# Step 2: Encrypt the AES key (optional, for secure key transfer)
encrypted_key_path = sender.encrypt_key(aes_key,'aes-key.enc')

# Step 3: Zip the encrypted file and encrypted key together
zip_path = sender.zip_package([encrypted_file_path, encrypted_key_path], "output_package.zip")

# Step 4: Upload the zip file to S3
bucket_name = "tihan-test"

sender.upload_to_s3(file_path='output_package.zip',
                           bucket_name='s3-test',
                           object_name='test.zip',
                           minio_endpoint='192.168.x.x:9000',
                           access_key='ACCESS-KEY',
                           secret_key='SECRET-KEY')



print("File encrypted, zipped, and uploaded to S3 successfully.")


```

### Receiver Side
```python
from tihan.sdv.securetransfer.rsa_utils import generate_private_key, generate_public_key
from tihan.sdv.securetransfer.file_transfer import FileReceiver

# # Generate RSA key pair for testing
private_key_file = generate_private_key()
public_key_file = generate_public_key(private_key_file)

# Decrypt the file recived

# Load the receiver's private key (as bytes)
with open(r"private_key.pem", "rb") as f:
    receiver_private_key = f.read()

# decrypt the key 
receiver = FileReceiver(receiver_private_key)
key = receiver.decrypt_key(r'test\aes-key.enc')
# decrypt the file

receiver.decrypt_file(r'test\encrypted_file.enc',key,r'test\decrypted_file.txt')

```

---

## 🧪 Running Tests

```sh
# Set PYTHONPATH to project root if needed
set PYTHONPATH=.
pytest tests/test-file-name

```
> 📌 **Note:**
> All the unit tests are well writen in the /tests directory

---
## 📁Project Structure

```sh

tihan_sdv/
│
├── tihan/
│   └── sdv/
│       ├── securetransfer/
│       │   └── [ca.py]
│       │   └── [aes_utils.py]
│       │   └── [rsa_utils.py]
│       │   └── [file_transfering.py]
│       │   └── [config.py]
│       ├── visualizer/
│       │   ├── [ultrasonic.py]
│       │   └── [parking_assist.py]
│       └── compression/
│           └── ...
├── tests/
│   ├── [test_ca.py]
│   ├── [test_aes_utils.py]
│   ├── [test_rsa_utils.py]
│   ├── [test_file_transfer.py]
│   ├── [test_ultrasonic.py]
│   └── [test_park_assist.py]
├── [requirements.txt]
├── [setup.py]
└── [README.md]
```



## 🤝 Contributing
Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.


## 📜 License
This project is licensed under the MIT License.


> ## 👤 Author
> **Arindam Chakraborty** 
>
> [![Linkedin](https://i.sstatic.net/gVE0j.png) LinkedIn](https://www.linkedin.com/in/arindm007)
&nbsp;
[![GitHub](https://i.sstatic.net/tskMh.png) GitHub](https://github.com/arindm007)


## 🌟 Acknowledgements
- TiHAN Foundation, IIT Hyderabad




