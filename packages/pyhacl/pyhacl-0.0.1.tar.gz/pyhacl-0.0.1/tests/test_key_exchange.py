import unittest
from pyhacl.key_exchange import curve25519

class TestKeyExchange(unittest.TestCase):
    def test_key_exchange_x25519(self):
        alice_sk = b'a' * 32
        alice_pk = curve25519.secret_to_public(alice_sk)

        bob_sk = b'b' * 32
        bob_pk = curve25519.secret_to_public(bob_sk)

        shared1 = curve25519.ecdh(alice_sk, bob_pk)
        shared2 = curve25519.ecdh(bob_sk, alice_pk)

        self.assertEqual(shared1, shared2)
