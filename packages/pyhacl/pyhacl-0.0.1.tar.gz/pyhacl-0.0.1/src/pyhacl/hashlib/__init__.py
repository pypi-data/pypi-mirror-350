from .sha1 import sha1
from .sha2 import sha224, sha256, sha384, sha512

_hashes = {
    Hash.name: Hash
    for Hash in (
        sha1,
        sha224, sha256, sha384, sha512,
    )
}

algorithms_guaranteed = algorithms_available = list(_hashes)
__all__ = algorithms_guaranteed + [
    'new',
    'algorithms_guaranteed',
    'algorithms_available'
]

def new(name, data=b'', *, usedforsecurity=None):
    if Hash := _hashes.get(name):
        return Hash(data)
    e = f'unsupported hash type {name}'
    raise ValueError(e)
