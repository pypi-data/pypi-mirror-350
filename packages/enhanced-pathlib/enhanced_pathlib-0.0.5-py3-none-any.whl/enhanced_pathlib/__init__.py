#!/usr/bin/env python3

'''Enhancements to Path from pathlib to support signatures, compression, etc.'''

# Copyright (c) 2025 RedHat Inc
# Copyright (c) 2025 Cambridge Greys Ltd
#
# Licensed under the BSD 3-clause License
#

from pathlib import PosixPath, Path
from gzip import GzipFile
import io
import sys

try:
    from Crypto.Hash import SHA224, SHA256, SHA384, SHA512 # SHA2 family
    from Crypto.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512 # SHA2 family
    from Crypto.Signature import pkcs1_15
except ModuleNotFoundError:
    from Cryptodome.Hash import SHA224, SHA256, SHA384, SHA512 # SHA2 family
    from Cryptodome.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512 # SHA2 family
    from Cryptodome.Signature import pkcs1_15

VERSION = "0.0.5"

COMPRESSION_HANDLERS = {
    'gzip':GzipFile
}

SIGNATURE_HANDLERS = {
    'sha224':SHA224,
    'sha256':SHA256,
    'sha384':SHA384,
    'sha512':SHA512,
    'sha3-224':SHA3_224,
    'sha3-256':SHA3_256,
    'sha3-384':SHA3_384,
    'sha3-512':SHA3_512,
}

class EPath(PosixPath):
    '''Enhanced Path class supporting compressed, signed and encrypted formats'''
    # pathlib initializes attributes in __new__ instead of init. We have to follow
    # this convention in order to descend from it. That is ugly, prohibited and and
    # an abbomination onto Nuggan. Nothing we can do about it short of disabling
    # the checks

    # pylint: disable=self-cls-assignment,return-in-init,inconsistent-return-statements
    def __new__(cls, *args, **kwargs):
        cls = EPath
        if sys.version_info[0] == 3 and sys.version_info[1] < 12:
            self = cls._from_parts(args)
            return self
        return object.__new__(cls)

    # The parent classes in pathlib initialize instance attribs in __new__ instead of __init__
    # We have to follow this convention, which requires leaving *args alone and not calling
    # parent's __init__(). This is seriously ugly, but nothing we can do about it.

    # pylint: disable=unused-argument
    def __init__(self, *args, signed=None, compress=None, signature=None, key=None):
        if sys.version_info[0] == 3 and sys.version_info[1] > 11:
            super().__init__(*args)
        self.signed = signed
        self.compress = compress
        self.signature = signature
        self.key = key

    def verify(self, data):
        '''Verify detached signature'''
        data_hash = SIGNATURE_HANDLERS[self.signed].new(data)
        # this raises Value Error if the signature does not match
        pkcs1_15.new(self.key).verify(data_hash, self.signature)

    def read_bytes(self):
        '''Read additional formats and present them as bytes'''

        # no, this does not work with with because you have a chain of
        # streams of variable length and with does not allow you to control
        # which and when will be close()-d

        # pylint: disable=consider-using-with

        fileobj = self.open(mode='rb')
        data = fileobj.read()
        fileobj.close()

        if self.signed is not None:
            self.verify(data)

        if self.compress is not None:
            data = COMPRESSION_HANDLERS[self.compress](fileobj=io.BytesIO(data)).read()

        return data


    def write_bytes(self, data):
        '''Write bytes in additional formats'''

        result = 0
        with self.open(mode='wb') as fileobj:
            if self.compress is not None:
                compressed = COMPRESSION_HANDLERS[self.compress](fileobj=fileobj, mode="wb")
                result = compressed.write(data)
                compressed.close()
            else:
                result = fileobj.write(data)

        return result

    def read_text(self, encoding=None, errors=None, newline=None):
        '''Read additional formats and present them as text'''

        if encoding is None:
            encoding = 'ascii'
        return str(self.read_bytes(), encoding=encoding)

    def write_text(self, data, encoding=None, errors=None, newline=None):
        '''Write in additional formats and present them as bytes'''

        if encoding is None:
            encoding = 'ascii'
        return self.write_bytes(data.encode(encoding))
