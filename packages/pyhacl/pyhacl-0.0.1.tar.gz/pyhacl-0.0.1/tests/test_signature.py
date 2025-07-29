import unittest
from parameterized import parameterized
from pyhacl.signature import p256

p256_priv = bytes.fromhex(
    '3813E9CC1168AED230DCA65AF0F0BF3EAF2D48A3495777A0D865D4CE1E0094E0')
p256_pub = bytes.fromhex(
    '7BD9F4AA8801613D81C73B9480347D0A6AB4AF7EB1B04EB634151477EB651ED6'
    'CBBC6251D01C0CD52E5FDC1B44C9AC544059FAC6398EE1DA4F4382E356A4D9C9')

class TestSignatureP256(unittest.TestCase):
    def test_sign_p256_key_valid(self):
        self.assertTrue(p256.validate_private_key(p256_priv))
        self.assertTrue(p256.validate_public_key(p256_pub))

    @parameterized.expand(('', '_sha2', '_sha256', '_sha384', '_sha512'))
    def test_sign_p256_verify(self, name):
        sign_func = getattr(p256, f'sign{name}')
        verif_func = getattr(p256, f'verif{name}')

        data = b'some data ' * 4
        nonce = b'a' * 32

        self.assertTrue(
            verif_func(data, p256_pub,
                sign_func(data, p256_priv, nonce)
            )
        )
