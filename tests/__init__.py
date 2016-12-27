import unittest
from jellyfish import *
import sys
class TestEncryptDecrypt(unittest.TestCase):
    def setUp(self):
        self.in_filename = '/tmp/crypt.tmp.in'
        self.out_filename = '/tmp/crypt.tmp.out'
        self.dec_filename = '/tmp/crypt.tmp.dec'
        self.key = 'testkey'

    def tearDown(self):
        self.remove_files(
            self.in_filename,
            self.out_filename,
            self.dec_filename,
        )

    def remove_files(self, *filenames):
        for fn in filenames:
            if os.path.exists(fn):
                os.unlink(fn)

    def write_bytes(self, num, ch='a'):
        buf = ch * num
        with open(self.in_filename, 'wb') as fh:
            fh.write(buf)
        return buf

    def crypt_data(self, num_bytes, ch, in_key=None, out_key=None, chunk_size=4096):
        in_key = in_key or self.key
        out_key = out_key or self.key

        buf = self.write_bytes(num_bytes, ch)
        encrypt_file(self.in_filename, self.out_filename, in_key, chunk_size)
        decrypt_file(self.out_filename, self.dec_filename, out_key, chunk_size)

        with open(self.dec_filename, 'rb') as fh:
            decrypted = fh.read()

        return buf, decrypted

    def test_encrypt_decrypt(self):
        def encrypt_flow(ch):
            for i in range(17):
                buf, decrypted = self.crypt_data(i, ch)
                self.assertEqual(buf, decrypted)

        encrypt_flow('a')
        encrypt_flow('\x00')
        encrypt_flow('\x01')
        encrypt_flow('\xff')

    def test_key(self):
        buf, decrypted = self.crypt_data(128, 'a', self.key, self.key+'x')
        self.assertNotEqual(buf, decrypted)

    def test_chunk_sizes(self):
        for i in [128, 1024, 2048, 4096]:
            nb = [i - 1, i, i + 1, i * 2, i * 2 + 1]
            for num_bytes in nb:
                buf, decrypted = self.crypt_data(num_bytes, 'a', chunk_size=i)
                self.assertEqual(buf, decrypted)

    def test_stringio(self):
        for i in [128, 1024, 2048, 4096]:
            nb = [i - 1, i, i + 1, i * 2, i * 2 + 1]
            for num_bytes in nb:
                in_buf = StringIO()
                out_buf = StringIO()
                dec_buf = StringIO()
                in_buf.write(num_bytes * 'a')
                in_buf.seek(0)
                encrypt(in_buf, out_buf, self.key, i)
                out_buf.seek(0)
                decrypt(out_buf, dec_buf, self.key, i)
                self.assertEqual(in_buf.getvalue(), dec_buf.getvalue())
unittest.main(argv=sys.argv[:1], verbosity=not options.quiet and 2 or 0)