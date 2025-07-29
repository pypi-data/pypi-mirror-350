import pathlib
import unittest
from parameterized import parameterized
from pyhacl.hashlib import sha1, sha224, sha256, sha384, sha512

shabytetestvectors_dir = pathlib.Path(__file__).parent.joinpath('shabytetestvectors')

class TestHashlib(unittest.TestCase):
    @parameterized.expand([
        (f'SHA{Hash.name[3:]}{suite}', Hash)
        for Hash in [sha1, sha224, sha256, sha384, sha512]
        for suite in ('Short', 'Long')
    ])
    def test_hashlib(self, name, Hash):
        with shabytetestvectors_dir.joinpath(f'{name}Msg.rsp').open() as file:
            header_lineno = 7
            for _ in range(header_lineno):
                file.readline()

            rl = iter(file.readline, '')
            for lineno, (Len, Msg, MD, _) in enumerate(zip(rl, rl, rl, rl)):
                with self.subTest(lineno=lineno * 4 + header_lineno + 1):
                    Len = int(Len.removeprefix('Len = ').strip()) // 8
                    Msg = bytes.fromhex(Msg.removeprefix('Msg = ').strip())
                    MD = MD.removeprefix('MD = ').strip()
                    if Len == 0 and Msg == b'\0':
                        Msg = b''
                    self.assertEqual(len(Msg), Len)  # safety check

                    sha = Hash()
                    for chunkno in range(0, Len, 256):
                        sha.update(Msg[chunkno:chunkno+256])
                    self.assertEqual(sha.digest(), bytes.fromhex(MD))
                    self.assertEqual(sha.hexdigest(), MD)
                    self.assertEqual(Hash.oneshot(Msg), bytes.fromhex(MD))
                    self.assertEqual(Hash.hexoneshot(Msg), MD)
