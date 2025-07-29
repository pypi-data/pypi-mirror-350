# distutils: sources = hacl-packages/src/Hacl_P256.c hacl-packages/src/Hacl_Hash_SHA2.c

import cython
from cython.cimports.libc.stdint import uint8_t

from cython.cimports.pyhacl.signature import p256

from pyhacl import HACLError


def validate_private_key(private_key: bytes) -> bool:
    if len(private_key) != 32:
        e = "private key must be a raw key 32 bytes long"
        raise ValueError(e)
    return p256.Hacl_P256_validate_private_key(
        cython.cast(cython.pointer(uint8_t), private_key),
    )


def validate_public_key(public_key: bytes) -> bool:
    if len(public_key) != 64:
        e = "public key must be a raw key 32 bytes long"
        raise ValueError(e)
    return p256.Hacl_P256_validate_public_key(
        cython.cast(cython.pointer(uint8_t), public_key),
    )


def sign(message: bytes, private_key: bytes, nonce: bytes) -> bytes:
    if len(message) < 32:
        e = "message must be at least 32 bytes long"
        raise ValueError(e)
    if len(private_key) != 32:
        e = "private key must be a raw key 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 32:
        e = "nonce must be 32 bytes long"
        raise ValueError(e)
    signature: uint8_t[64]
    ok: bool = p256.Hacl_P256_ecdsa_sign_p256_without_hash(
        signature,
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), private_key),
        cython.cast(cython.pointer(uint8_t), nonce),
    )
    if not ok:
        e = "signature failed"
        raise HACLError(e)
    return signature[:64]


def sign_sha256(message: bytes, private_key: bytes, nonce: bytes) -> bytes:
    if len(private_key) != 32:
        e = "private key must be a raw key 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 32:
        e = "nonce must be 32 bytes long"
        raise ValueError(e)
    signature: uint8_t[64]
    ok: bool = p256.Hacl_P256_ecdsa_sign_p256_sha2(
        signature,
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), private_key),
        cython.cast(cython.pointer(uint8_t), nonce),
    )
    if not ok:
        e = "signature failed"
        raise HACLError(e)
    return signature[:64]

sign_sha2 = sign_sha256


def sign_sha384(message: bytes, private_key: bytes, nonce: bytes) -> bytes:
    if len(private_key) != 32:
        e = "private key must be a raw key 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 32:
        e = "nonce must be 32 bytes long"
        raise ValueError(e)
    signature: uint8_t[64]
    ok: bool = p256.Hacl_P256_ecdsa_sign_p256_sha384(
        signature,
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), private_key),
        cython.cast(cython.pointer(uint8_t), nonce),
    )
    if not ok:
        e = "signature failed"
        raise HACLError(e)
    return signature[:64]


def sign_sha512(message: bytes, private_key: bytes, nonce: bytes) -> bytes:
    if len(private_key) != 32:
        e = "private key must be a raw key 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 32:
        e = "nonce must be 32 bytes long"
        raise ValueError(e)
    signature: uint8_t[64]
    ok: bool = p256.Hacl_P256_ecdsa_sign_p256_sha512(
        signature,
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), private_key),
        cython.cast(cython.pointer(uint8_t), nonce),
    )
    if not ok:
        e = "signature failed"
        raise HACLError(e)
    return signature[:64]



def verif(message: bytes, public_key: bytes, signature: bytes) -> bool:
    if len(message) < 32:
        e = "message must be at least 32 bytes long"
        raise ValueError(e)
    if len(public_key) != 64:
        e = "public key myst be a raw key 64 bytes long"
        raise ValueError(e)
    if len(signature) != 64:
        e = "signature must be 64 bytes long"
        raise ValueError(e)
    signarure_r: uint8_t[32] = signature[:32]
    signature_s: uint8_t[32] = signature[32:]
    return p256.Hacl_P256_ecdsa_verif_without_hash(
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), public_key),
        signarure_r,
        signature_s,
    )


def verif_sha256(message: bytes, public_key: bytes, signature: bytes) -> bool:
    if len(public_key) != 64:
        e = "public key myst be a raw key 64 bytes long"
        raise ValueError(e)
    if len(signature) != 64:
        e = "signature must be 64 bytes long"
        raise ValueError(e)
    signarure_r: uint8_t[32] = signature[:32]
    signature_s: uint8_t[32] = signature[32:]
    return p256.Hacl_P256_ecdsa_verif_p256_sha2(
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), public_key),
        signarure_r,
        signature_s,
    )

verif_sha2 = verif_sha256


def verif_sha384(message: bytes, public_key: bytes, signature: bytes) -> bool:
    if len(public_key) != 64:
        e = "public key myst be a raw key 64 bytes long"
        raise ValueError(e)
    if len(signature) != 64:
        e = "signature must be 64 bytes long"
        raise ValueError(e)
    signarure_r: uint8_t[32] = signature[:32]
    signature_s: uint8_t[32] = signature[32:]
    return p256.Hacl_P256_ecdsa_verif_p256_sha384(
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), public_key),
        signarure_r,
        signature_s,
    )


def verif_sha512(message: bytes, public_key: bytes, signature: bytes) -> bool:
    if len(public_key) != 64:
        e = "public key myst be a raw key 64 bytes long"
        raise ValueError(e)
    if len(signature) != 64:
        e = "signature must be 64 bytes long"
        raise ValueError(e)
    signarure_r: uint8_t[32] = signature[:32]
    signature_s: uint8_t[32] = signature[32:]
    return p256.Hacl_P256_ecdsa_verif_p256_sha512(
        len(message),
        cython.cast(cython.pointer(uint8_t), message),
        cython.cast(cython.pointer(uint8_t), public_key),
        signarure_r,
        signature_s,
    )
