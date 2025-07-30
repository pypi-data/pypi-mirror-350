import os
import subprocess

class CertificateAuthority:

    def __init__(self, name):
        self.name = name
        self.certificates = []

    def issue_certificate(self, certificate):
        self.certificates.append(certificate)
        print(f"Certificate {certificate} issued by {self.name}")

    def revoke_certificate(self, certificate):
        if certificate in self.certificates:
            self.certificates.remove(certificate)
            print(f"Certificate {certificate} revoked by {self.name}")
        else:
            print(f"Certificate {certificate} not found in CA {self.name}")

    def list_certificates(self):
        print(f"Certificates issued by {self.name}:")
        for cert in self.certificates:
            print(cert)
        return self.certificates

    def generate_private_key(self, key_size=2048):
        private_key_file = f"{self.name}_private_key.pem"
        subprocess.run(["openssl", "genrsa", "-out", private_key_file, str(key_size)])
        return private_key_file

    def generate_public_key(self, private_key_file):
        public_key_file = f"{self.name}_public_key.pem"
        subprocess.run(["openssl", "rsa", "-pubout", "-in", private_key_file, "-out", public_key_file])
        return public_key_file

    def generate_certificate_signing_request(self, private_key_file, common_name, country, state, locality, organization, organizational_unit):
        csr_file = f"{self.name}_csr.pem"
        subprocess.run([
            "openssl", "req", "-new", "-key", private_key_file, "-out", csr_file,
            "-subj", f"/C={country}/ST={state}/L={locality}/O={organization}/OU={organizational_unit}/CN={common_name}"
        ])
        return csr_file

    def sign_certificate(self, csr_file, private_key_file, days=365):
        certificate_file = f"{self.name}_certificate.pem"
        subprocess.run([
            "openssl", "x509", "-req", "-in", csr_file, "-signkey", private_key_file,
            "-out", certificate_file, "-days", str(days)
        ])
        return certificate_file

    def generate_self_signed_certificate(self, common_name, country, state, locality, organization, organizational_unit):
        private_key_file = self.generate_private_key()
        csr_file = self.generate_certificate_signing_request(private_key_file, common_name, country, state, locality, organization, organizational_unit)
        certificate_file = self.sign_certificate(csr_file, private_key_file)
        return private_key_file, certificate_file

    def load_certificate(self, certificate_file):
        with open(certificate_file, "r") as file:
            certificate = file.read()
        return certificate

    def load_private_key(self, private_key_file):
        with open(private_key_file, "r") as file:
            private_key = file.read()
        return private_key

    def load_public_key(self, public_key_file):
        with open(public_key_file, "r") as file:
            public_key = file.read()
        return public_key

    def verify_certificate(self, certificate, certificate_file):
        with open("temp_cert.pem", "w") as cert_file:
            cert_file.write(certificate)
        result = subprocess.run([
            "openssl", "verify", "-CAfile", certificate_file, "temp_cert.pem"
        ], capture_output=True, text=True)
        os.remove("temp_cert.pem")
        return result.returncode == 0