jellyfish
=======

.. image:: https://travis-ci.org/wannaphongcom/jellyfish.svg?branch=master

Easy file encryption using pycryptodome

forked from coleifer/beefish https://github.com/coleifer/beefish

.. image:: https://i.imgur.com/RT38mUS.jpg

installing
----------

::

    pip install pycryptodome

Alternatively::

    pip install -e git+git://github.com/wannaphongcom/jellyfish.git#egg=beefish

Dependencies:

* `pycryptodome <https://pycryptodome.readthedocs.io/>`_


usage
-----

jellyfish can be used to encrypt and decrypt file-like objects::

    from jellyfish import encrypt, decrypt

    # encrypting
    with open('secrets.txt') as fh:
        with open('secrets.enc', 'wb') as out_fh:
            encrypt(fh, out_fh, 'secret p@ssword')

    # decrypting
    with open('secrets.enc') as fh:
        with open('secrets.dec', 'wb') as out_fh:
            decrypt(fh, out_fh, 'secret p@ssword')

you can use a shortcut if you like::

    # encrypting
    encrypt_file('secrets.txt', 'secrets.enc', 'p@ssword')

    # decrypting
    decrypt_file('secrets.enc', 'secrets.dec', 'p@ssword')


you can use it from the command-line::

    jellyfish.py -e secrets.txt secrets.enc
    jellyfish.py -d secrets.enc secrets.dec
