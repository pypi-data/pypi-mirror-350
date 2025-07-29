# distutils: sources = hacl-packages/src/Hacl_Curve25519_51.c

from cython.cimports.libc.stdint import uint8_t
from cython.cimports.pyhacl.key_exchange import curve25519

from pyhacl import HACLError


def scalarmult(secret_key: bytes, public_key: bytes) -> bytes:
    if len(secret_key) != 32:
        e = "secret_key must be 32 bytes long"
        raise ValueError(e)
    if len(public_key) != 32:
        e = "public_key must be 32 bytes long"
        raise ValueError(e)
    skey: uint8_t[32] = secret_key
    pkey: uint8_t[32] = public_key
    point: uint8_t[32]
    curve25519.Hacl_Curve25519_51_scalarmult(point, skey, pkey)
    return point[:32]


def secret_to_public(secret_key: bytes) -> bytes:
    if len(secret_key) != 32:
        e = "secret_key must be 32 bytes long"
        raise ValueError(e)
    skey: uint8_t[32] = secret_key
    pkey: uint8_t[32]
    curve25519.Hacl_Curve25519_51_secret_to_public(pkey, skey)
    return pkey[:32]


def ecdh(secret_key: bytes, public_key: bytes) -> bytes:
    if len(secret_key) != 32:
        e = "secret_key must be 32 bytes long"
        raise ValueError(e)
    if len(public_key) != 32:
        e = "public_key must be 32 bytes long"
        raise ValueError(e)
    skey: uint8_t[32] = secret_key
    pkey: uint8_t[32] = public_key
    shared_key: uint8_t[32]
    ok: bool = curve25519.Hacl_Curve25519_51_ecdh(shared_key, skey, pkey)
    if not ok:
        e = "creation of a shared key failed"
        raise HACLError(e)
    return shared_key[:32]
