# distutils: sources = hacl-packages/src/Hacl_Hash_SHA1.c

import cython
from cython.cimports.libc.stdint import uint8_t
from cython.cimports.libc.string import memcpy

from cython.cimports.pyhacl.hashlib import sha1 as sha1lib


@cython.cclass
class sha1:
    name = 'sha1'
    block_size = 64
    digest_size = 20

    _state: cython.pointer(sha1lib.Hacl_Hash_SHA1_state_t)

    def __cinit__(self):
        self._state = sha1lib.Hacl_Hash_SHA1_malloc()
        if not self._state:
            raise MemoryError()

    def __dealloc__(self):
        sha1lib.Hacl_Hash_SHA1_free(self._state)
        self._state = cython.NULL

    def __init__(self, data=b''):
        super().__init__()
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        sha1lib.Hacl_Hash_SHA1_update(
            self._state,
            cython.cast(cython.pointer(uint8_t), data),
            len(data),
        )

    def digest(self) -> bytes:
        output: uint8_t[20]
        sha1lib.Hacl_Hash_SHA1_digest(self._state, output)
        return output[:20]

    def hexdigest(self) -> str:
        return self.digest().hex()

    def copy(self):
        copy: sha1 = type(self)()
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
        output: cython.char[20]
        sha1lib.Hacl_Hash_SHA1_hash(
            cython.cast(cython.pointer(uint8_t), output),
            cython.cast(cython.pointer(uint8_t), data),
            len(data)
        )
        return output[:20]

    @classmethod
    def hexoneshot(cls, data: bytes) -> str:
        return cls.oneshot(data).hex()
