# distutils: sources = hacl-packages/src/Hacl_Hash_SHA2.c

import cython
from cython.cimports.libc.stdint import uint8_t
from cython.cimports.libc.string import memcpy

from cython.cimports.pyhacl.hashlib import sha2


@cython.cclass
class sha224:
    name = 'sha224'
    block_size = 64
    digest_size = 28

    _state: cython.pointer(sha2.Hacl_Hash_SHA2_state_t_224)

    def __cinit__(self):
        self._state = sha2.Hacl_Hash_SHA2_malloc_224()
        if not self._state:
            raise MemoryError()

    def __dealloc__(self):
        sha2.Hacl_Hash_SHA2_free_224(self._state)
        self._state = cython.NULL

    def __init__(self, data=b''):
        super().__init__()
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        sha2.Hacl_Hash_SHA2_update_224(
            self._state,
            cython.cast(cython.pointer(uint8_t), data),
            len(data),
        )

    def digest(self) -> bytes:
        output: uint8_t[28]
        sha2.Hacl_Hash_SHA2_digest_224(self._state, output)
        return output[:28]

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self):
        copy: sha224 = type(self)()
        copy._state[0].block_state[0] = self._state[0].block_state[0]
        memcpy(
            cython.cast(cython.p_void, copy._state[0].buf),
            cython.cast(cython.p_void, self._state[0].buf),
            64,
        )
        copy._state[0].total_len = self._state[0].total_len
        return copy

    @classmethod
    def oneshot(cls, data: bytes) -> bytes:
        output: cython.char[28]
        sha2.Hacl_Hash_SHA2_hash_224(
            cython.cast(cython.pointer(uint8_t), output),
            cython.cast(cython.pointer(uint8_t), data),
            len(data)
        )
        return output[:28]

    @classmethod
    def hexoneshot(cls, data: bytes) -> str:
        return cls.oneshot(data).hex()


@cython.cclass
class sha256:
    name = 'sha256'
    block_size = 64
    digest_size = 32

    _state: cython.pointer(sha2.Hacl_Hash_SHA2_state_t_256)

    def __cinit__(self):
        self._state = sha2.Hacl_Hash_SHA2_malloc_256()
        if not self._state:
            raise MemoryError()

    def __dealloc__(self):
        sha2.Hacl_Hash_SHA2_free_256(self._state)
        self._state = cython.NULL

    def __init__(self, data=b''):
        super().__init__()
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        sha2.Hacl_Hash_SHA2_update_256(
            self._state,
            cython.cast(cython.pointer(uint8_t), data),
            len(data),
        )

    def digest(self) -> bytes:
        output: uint8_t[32]
        sha2.Hacl_Hash_SHA2_digest_256(self._state, output)
        return output[:32]

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self):
        copy: sha256 = type(self)()
        copy._state[0].block_state[0] = self._state[0].block_state[0]
        memcpy(
            cython.cast(cython.p_void, copy._state[0].buf),
            cython.cast(cython.p_void, self._state[0].buf),
            64,
        )
        copy._state[0].total_len = self._state[0].total_len
        return copy

    @classmethod
    def oneshot(cls, data: bytes) -> bytes:
        output: cython.char[32]
        sha2.Hacl_Hash_SHA2_hash_256(
            cython.cast(cython.pointer(uint8_t), output),
            cython.cast(cython.pointer(uint8_t), data),
            len(data)
        )
        return output[:32]

    @classmethod
    def hexoneshot(cls, data: bytes) -> str:
        return cls.oneshot(data).hex()


@cython.cclass
class sha384:
    name = 'sha384'
    block_size = 128
    digest_size = 48

    _state: cython.pointer(sha2.Hacl_Hash_SHA2_state_t_384)

    def __cinit__(self):
        self._state = sha2.Hacl_Hash_SHA2_malloc_384()
        if not self._state:
            raise MemoryError()

    def __dealloc__(self):
        sha2.Hacl_Hash_SHA2_free_384(self._state)
        self._state = cython.NULL

    def __init__(self, data=b''):
        super().__init__()
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        sha2.Hacl_Hash_SHA2_update_384(
            self._state,
            cython.cast(cython.pointer(uint8_t), data),
            len(data),
        )

    def digest(self) -> bytes:
        output: uint8_t[48]
        sha2.Hacl_Hash_SHA2_digest_384(self._state, output)
        return output[:48]

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self):
        copy: sha384 = type(self)()
        copy._state[0].block_state[0] = self._state[0].block_state[0]
        memcpy(
            cython.cast(cython.p_void, copy._state[0].buf),
            cython.cast(cython.p_void, self._state[0].buf),
            128,
        )
        copy._state[0].total_len = self._state[0].total_len
        return copy

    @classmethod
    def oneshot(cls, data: bytes) -> bytes:
        output: cython.char[48]
        sha2.Hacl_Hash_SHA2_hash_384(
            cython.cast(cython.pointer(uint8_t), output),
            cython.cast(cython.pointer(uint8_t), data),
            len(data)
        )
        return output[:48]

    @classmethod
    def hexoneshot(cls, data: bytes) -> str:
        return cls.oneshot(data).hex()


@cython.cclass
class sha512:
    name = 'sha512'
    block_size = 128
    digest_size = 64

    _state: cython.pointer(sha2.Hacl_Hash_SHA2_state_t_512)

    def __cinit__(self):
        self._state = sha2.Hacl_Hash_SHA2_malloc_512()
        if not self._state:
            raise MemoryError()

    def __dealloc__(self):
        sha2.Hacl_Hash_SHA2_free_512(self._state)
        self._state = cython.NULL

    def __init__(self, data=b''):
        super().__init__()
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        sha2.Hacl_Hash_SHA2_update_512(
            self._state,
            cython.cast(cython.pointer(uint8_t), data),
            len(data),
        )

    def digest(self) -> bytes:
        output: uint8_t[64]
        sha2.Hacl_Hash_SHA2_digest_512(self._state, output)
        return output[:64]

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self):
        copy: sha512 = type(self)()
        copy._state[0].block_state[0] = self._state[0].block_state[0]
        memcpy(
            cython.cast(cython.p_void, copy._state[0].buf),
            cython.cast(cython.p_void, self._state[0].buf),
            128,
        )
        copy._state[0].total_len = self._state[0].total_len
        return copy

    @classmethod
    def oneshot(cls, data: bytes) -> bytes:
        output: cython.char[64]
        sha2.Hacl_Hash_SHA2_hash_512(
            cython.cast(cython.pointer(uint8_t), output),
            cython.cast(cython.pointer(uint8_t), data),
            len(data)
        )
        return output[:64]

    @classmethod
    def hexoneshot(cls, data: bytes) -> str:
        return cls.oneshot(data).hex()
