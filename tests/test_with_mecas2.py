from __future__ import unicode_literals, absolute_import, print_function
from . import Pyas2TestCase, as2
import os


class TestMecAS2(Pyas2TestCase):

    def setUp(self):
        self.org = as2.Organization(
            as2_name='some_organization',
            sign_key=self.private_key,
            sign_key_pass='test',
            decrypt_key=self.private_key,
            decrypt_key_pass='test'
        )
        self.partner = as2.Partner(
            as2_name='mecas2',
            verify_cert=self.mecas2_public_key,
            encrypt_cert=self.mecas2_public_key,
            validate_certs=False
        )

    def test_compressed_message(self):
        """ Test Compressed Message received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(self.TEST_DIR, 'mecas2_compressed.as2')
        with open(received_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.compressed)
        self.assertEqual(self.test_data, in_message.content)

    def test_encrypted_message(self):
        """ Test Encrypted Message received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(self.TEST_DIR, 'mecas2_encrypted.as2')
        with open(received_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypted)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertEqual(self.test_data, in_message.content)

    def test_signed_message(self):
        """ Test Unencrypted Signed Uncompressed Message from Mendelson AS2"""
        # Parse the generated AS2 message as the partner
        received_file = os.path.join(self.TEST_DIR, 'mecas2_signed.as2')
        with open(received_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.signed)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(self.test_data, in_message.content)

    def test_encrypted_signed_message(self):
        """ Test Encrypted Signed Uncompressed Message from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(
            self.TEST_DIR, 'mecas2_signed_encrypted.as2')
        with open(received_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypted)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertTrue(in_message.signed)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(self.test_data, in_message.content)

    def test_encrypted_signed_compressed_message(self):
        """ Test Encrypted Signed Compressed Message from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(
            self.TEST_DIR, 'mecas2_compressed_signed_encrypted.as2')
        with open(received_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypted)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertTrue(in_message.signed)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(self.test_data, in_message.content)

    def test_unsigned_mdn(self):
        """ Test Unsigned MDN received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(self.TEST_DIR, 'mecas2_unsigned.mdn')
        with open(received_file, 'rb') as fp:
            in_message = as2.Mdn()
            status, detailed_status = in_message.parse(
                fp.read(), find_message_cb=self.find_message)

        self.assertEqual(status, 'processed/error')
        self.assertEqual(detailed_status, 'authentication-failed')

    def test_signed_mdn(self):
        """ Test Signed MDN received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        received_file = os.path.join(self.TEST_DIR, 'mecas2_signed.mdn')
        with open(received_file, 'rb') as fp:
            in_message = as2.Mdn()
            in_message.parse(fp.read(), find_message_cb=self.find_message)

    def find_org(self, headers):
        return self.org

    def find_partner(self, headers):
        return self.partner

    def find_message(self, message_id, message_recipient):
        message = as2.Message()
        message.sender = self.org
        message.receiver = self.partner
        message.mic = b'O4bvrm5t2YunRfwvZicNdEUmPaPZ9vUslX8loVLDck0='
        return message
