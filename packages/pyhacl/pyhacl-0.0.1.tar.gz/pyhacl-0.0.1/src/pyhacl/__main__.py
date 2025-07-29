import os
import sys

from .aead import chacha_poly1305
from .hashlib import sha1, sha256, sha384, sha512
from .key_exchange import curve25519_64
from .signature import p256

def main():
    data = b"Hello world!"

    print("pyhacl demo", data)

    # Hashlib
    sha = sha256.oneshot(data)
    print(
        "\nHashlib"
        "\nsha1", sha1.oneshot(data).hex(),
        "\nsha256", sha.hex(),
        "\nsha384", sha384.oneshot(data).hex(),
        "\nsha512", sha512.oneshot(data).hex(),
    )

    # AEAD
    key32 = os.urandom(32)
    nonce12 = b'\x01' * 12
    cipher, tag = chacha_poly1305.encrypt(
        data, sha, key32, nonce12
    )
    text = chacha_poly1305.decrypt(
        cipher, sha, key32, nonce12, tag
    )
    print(
      "\nAEAD"
      "\nchapoly"
      "\n\trandom key", key32.hex(),
      "\n\tnonce", nonce12.hex(),
      "\n\tcipher", cipher.hex(),
      "\n\ttag", tag.hex(),
      "\n\tdecrypted back", text,
    )

    # Signature
    p256_priv = bytes.fromhex(
        '3813E9CC1168AED230DCA65AF0F0BF3EAF2D48A3495777A0D865D4CE1E0094E0')
    assert p256.validate_private_key(p256_priv)
    p256_pub = bytes.fromhex(
        '7BD9F4AA8801613D81C73B9480347D0A6AB4AF7EB1B04EB634151477EB651ED6'
        'CBBC6251D01C0CD52E5FDC1B44C9AC544059FAC6398EE1DA4F4382E356A4D9C9')
    assert p256.validate_public_key(p256_pub)

    nonce32 = b'\x01' * 32
    signature = p256.sign_sha256(cipher, p256_priv, nonce32)
    assert p256.verif_sha256(cipher, p256_pub, signature)
    print(
        "\nSignature"
        "\np256"
        "\n\tpriv", p256_priv.hex(),
        "\n\tpub", p256_pub.hex(),
        "\n\tnonce", nonce32.hex(),
        "\n\tsigned sha256", signature.hex(),
        "\n\tsignature validates"
    )

    # Key exchange
    alice_priv = os.urandom(32)
    alice_pub = curve25519_64.secret_to_public(alice_priv)
    bob_priv = os.urandom(32)
    bob_pub = curve25519_64.secret_to_public(bob_priv)
    alice_shared = curve25519_64.ecdh(alice_priv, bob_pub)
    bob_shared = curve25519_64.ecdh(bob_priv, alice_pub)
    print(
        "\nKey Exchange",
        "\nx22519"
        "\n\talice priv", alice_priv.hex(),
        "\n\talice pub", alice_pub.hex(),
        "\n\tbob priv", bob_priv.hex(),
        "\n\tbob pub", bob_pub.hex(),
        "\n\talice shared", alice_shared.hex(),
        "\n\tbob shared  ", bob_shared.hex(),
    )


sys.exit(main())
