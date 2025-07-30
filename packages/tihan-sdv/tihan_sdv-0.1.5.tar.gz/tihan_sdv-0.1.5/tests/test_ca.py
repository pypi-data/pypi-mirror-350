import unittest
from tihan.sdv.securetransfer.ca import CertificateAuthority
import os
import subprocess


class TestCertificateAuthority(unittest.TestCase):

    def setUp(self):
        self.ca = CertificateAuthority("TestCA")
        self.private_key_file, self.certificate_file = self.ca.generate_self_signed_certificate(
            common_name="test.com",
            country="US",
            state="California",
            locality="Los Angeles",
            organization="Test Org",
            organizational_unit="IT"
        )
        self.public_key_file = self.ca.generate_public_key(self.private_key_file)

    def test_issue_certificate(self):
        self.ca.issue_certificate("test_certificate")
        self.assertIn("test_certificate", self.ca.certificates)

    def test_revoke_certificate(self):
        self.ca.issue_certificate("test_certificate")
        self.ca.revoke_certificate("test_certificate")
        self.assertNotIn("test_certificate", self.ca.certificates)

    def test_list_certificates(self):
        self.ca.issue_certificate("test_certificate")
        self.ca.issue_certificate("another_certificate")
        certificates = self.ca.list_certificates()
        self.assertIn("test_certificate", certificates)
        self.assertIn("another_certificate", certificates)

    def test_verify_certificate(self):
        certificate = self.ca.load_certificate(self.certificate_file)
        result = self.ca.verify_certificate(certificate, self.certificate_file)
        self.assertTrue(result)

    def tearDown(self):
        import os
        os.remove(self.private_key_file)
        os.remove(self.certificate_file)
        os.remove(self.public_key_file)

if __name__ == "__main__":
    unittest.main()