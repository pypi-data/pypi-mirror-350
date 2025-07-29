# distutils: sources = hacl-packages/src/Hacl_AEAD_Chacha20Poly1305.c hacl-packages/src/Hacl_Chacha20.c hacl-packages/src/Hacl_MAC_Poly1305.c

import cython
from cython.cimports.libc.stdint import uint8_t
from cython.cimports.libc.stdlib import malloc, free

from cython.cimports.pyhacl.aead import chacha_poly1305

from pyhacl import HACLError


def encrypt(input: bytes, data: bytes, key: bytes, nonce: bytes) -> tuple[bytes, bytes]:
    if len(key) != 32:
        e = "key must be 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 12:
        e = "nonce must be 12 bytes long"
        raise ValueError(e)
    output: cython.pointer(uint8_t) = cython.cast(
        cython.pointer(uint8_t), malloc(len(input))
    )
    tag: uint8_t[16]
    chacha_poly1305.Hacl_AEAD_Chacha20Poly1305_encrypt(
        output,
        tag,
        cython.cast(cython.pointer(uint8_t), input),
        len(input),
        cython.cast(cython.pointer(uint8_t), data),
        len(data),
        cython.cast(cython.pointer(uint8_t), key),
        cython.cast(cython.pointer(uint8_t), nonce),
    )
    cipher: bytes = output[:len(input)]
    free(output)
    return (cipher, tag[:16])

def decrypt(input: bytes, data: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
    if len(key) != 32:
        e = "key must be 32 bytes long"
        raise ValueError(e)
    if len(nonce) != 12:
        e = "nonce must be 12 bytes long"
        raise ValueError(e)
    if len(tag) != 16:
        e = "tag must be 16 bytes long"
        raise ValueError(e)
    output: cython.pointer(uint8_t) = cython.cast(
        cython.pointer(uint8_t), malloc(len(input))
    )
    ko: bool = chacha_poly1305.Hacl_AEAD_Chacha20Poly1305_decrypt(
        output,
        cython.cast(cython.pointer(uint8_t), input),
        len(input),
        cython.cast(cython.pointer(uint8_t), data),
        len(data),
        cython.cast(cython.pointer(uint8_t), key),
        cython.cast(cython.pointer(uint8_t), nonce),
        cython.cast(cython.pointer(uint8_t), tag),
    )
    if ko:
        e = "decryption failed"
        raise HACLError(e)
    plain: bytes = output[:len(input)]
    free(output)
    return plain
