#!/usr/bin/env python
import getpass
import optparse
import os
import struct
import sys
from random import randrange
import six
PY3 = sys.version_info[0] == 3
if PY3:
    import builtins
    print_ = getattr(builtins, 'print')
    raw_input = getattr(builtins, 'input')
else:
    def print_(s):
        sys.stdout.write(s)
        sys.stdout.write('\n')

from six.moves import cStringIO as StringIO

from Crypto.Cipher import Blowfish
from Crypto import Random


def _gen_padding(file_size, block_size):
    pad_bytes = block_size - (file_size % block_size)
    padding = Random.get_random_bytes(pad_bytes - 1)
    bflag = randrange(block_size - 2, 256 - block_size)
    bflag -= bflag % block_size - pad_bytes
    return padding + six.int2byte(bflag)

def _read_padding(buffer, block_size):
	if PY3:
		return (buffer[-1] % block_size) or block_size
	else:
		return (ord(buffer[-1]) % block_size) or block_size

def generate_iv(block_size):
    return Random.get_random_bytes(block_size)

def get_cipher(key, iv):
    return Blowfish.new(key, Blowfish.MODE_CBC, iv)

def encrypt(in_buf, out_buf, key, chunk_size=4096):
    iv = generate_iv(Blowfish.block_size)
    cipher = get_cipher(key, iv)
    bytes_read = 0
    wrote_padding = False

    out_buf.write(iv)

    while 1:
        buffer = in_buf.read(chunk_size)
        buffer_len = len(buffer)
        bytes_read += buffer_len
        if buffer:
            if buffer_len < chunk_size:
                buffer += _gen_padding(bytes_read, cipher.block_size)
                wrote_padding = True
            out_buf.write(cipher.encrypt(buffer))
        else:
            if not wrote_padding:
                out_buf.write(cipher.encrypt(_gen_padding(bytes_read, cipher.block_size)))
            break

def decrypt(in_buf, out_buf, key, chunk_size=4096):
    iv = in_buf.read(Blowfish.block_size)

    cipher = get_cipher(key, iv)
    decrypted = ''

    while 1:
        buffer = in_buf.read(chunk_size)
        if buffer:
            decrypted = cipher.decrypt(buffer)
            out_buf.write(decrypted)
        else:
            break

    if decrypted:
        padding = _read_padding(decrypted, cipher.block_size)
        out_buf.seek(-padding, 2)
        out_buf.truncate()

def encrypt_file(in_file, out_file, key, chunk_size=4096):
    with open(in_file, 'rb') as in_fh:
        with open(out_file, 'wb') as out_fh:
            encrypt(in_fh, out_fh, key, chunk_size)

def decrypt_file(in_file, out_file, key, chunk_size=4096):
    with open(in_file, 'rb') as in_fh:
        with open(out_file, 'wb') as out_fh:
            decrypt(in_fh, out_fh, key, chunk_size)



if __name__ == '__main__':
    parser = optparse.OptionParser(usage='%prog [-e|-d] INFILE OUTFILE')
    parser.add_option('-t', '--test', dest='run_tests', action='store_true')
    parser.add_option('-k', '--key', dest='key', action='store', type='str')
    parser.add_option('-e', '--encrypt', dest='encrypt', action='store_true')
    parser.add_option('-d', '--decrypt', dest='decrypt', action='store_true')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true')
    (options, args) = parser.parse_args()

    if options.run_tests:
        unittest.main(argv=sys.argv[:1], verbosity=not options.quiet and 2 or 0)

    if len(args) == 1:
        if options.encrypt:
            default = '%s.e' % args[0]
        else:
            default = args[0].rstrip('.e')
        args.append(raw_input('Destination? (%s) ' % default) or default)

    if len(args) < 2 or not (options.encrypt or options.decrypt):
        parser.print_help()
        sys.exit(1)

    if not options.key:
        while 1:
            key = getpass.getpass('Key: ')
            verify = getpass.getpass('Verify: ')
            if key == verify:
                break
            else:
                print_('Keys did not match')
    else:
        key = options.key

    infile, outfile = args[0], args[1]
    if os.path.exists(outfile):
        print_('%s will be overwritten' % outfile)
        if raw_input('Continue? yN ') != 'y':
            sys.exit(2)

    if options.encrypt:
        encrypt_file(infile, outfile, key)
    else:
        decrypt_file(infile, outfile, key)
