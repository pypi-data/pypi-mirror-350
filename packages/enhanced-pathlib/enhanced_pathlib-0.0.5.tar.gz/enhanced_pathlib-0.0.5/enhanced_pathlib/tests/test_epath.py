#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Test cases for the enhanced pathlib module'''

from pathlib import Path
from tempfile import mkstemp
import os

from enhanced_pathlib import EPath
try:
    from Crypto.PublicKey import RSA
except ModuleNotFoundError:
    from Cryptodome.PublicKey import RSA

from nose.tools import ok_ as assert_
from nose.tools import raises
from nose.tools import assert_equal
from nose.tools import assert_is_none

KEY_NAME = 'testpublickey.pem'
SIG_NAME = 'test1.sig'
SIG_GZ_NAME = 'test1.gz.sig'
COMPRESSED1 = 'test1.gz'
COMPRESSED2 = 'test2.gz'
UNCOMPRESSED1 = 'test1'
UNCOMPRESSED2 = 'test2'


def load_sig(sig):
    '''Load signature'''
    with open(sig, mode="rb") as sigf:
        return sigf.read()

def load_key(key):
    '''Load public key'''
    with open(key) as keyf:
        return RSA.import_key(keyf.read())

def get_data(filename):
    '''Get filename data for the test'''
    return Path(filename).read_bytes()

def test_load_binary1():
    '''Load Binary file. This calls ancestor, should not generate an error'''
    e = EPath(UNCOMPRESSED1)
    assert_equal(e.read_bytes(), get_data(UNCOMPRESSED1))

def test_load_compressed1():
    '''Load Compressed file.'''
    e = EPath(COMPRESSED1, compress='gzip')
    assert_equal(e.read_bytes(), get_data(UNCOMPRESSED1))

def test_load_compressed2():
    '''Load Compressed file 2.''' 
    e = EPath(COMPRESSED2, compress='gzip')
    assert_(e.read_bytes() != get_data(UNCOMPRESSED1))

def test_load_signed():
    '''Load file. Pass signature'''
    e = EPath(UNCOMPRESSED1, signature=load_sig(SIG_NAME), key=load_key(KEY_NAME))
    assert_equal(e.read_bytes(), get_data(UNCOMPRESSED1))

def test_load_signed_wrong_sig():
    '''Load file. Fail signature'''
    e = EPath(UNCOMPRESSED2, signature=load_sig(SIG_NAME), key=load_key(KEY_NAME))
    try:
        e.read_bytes()
    except ValueError:
        pass

def test_load_signed_compressed():
    '''Load Compressed file. Check signature'''
    e = EPath(COMPRESSED1, signature=load_sig(SIG_GZ_NAME), key=load_key(KEY_NAME))
    assert_(e.read_bytes() != get_data(UNCOMPRESSED1))

def test_write_compressed():
    '''Write Compressed file.'''
    (handle, filename) = mkstemp(suffix=".gz", prefix="test_epath", dir="/tmp")

    e = EPath(filename, compress='gzip')
    e.write_bytes(get_data(UNCOMPRESSED1))

    r = EPath(filename, compress='gzip')

    assert_equal(e.read_bytes(), get_data(UNCOMPRESSED1))
    os.remove(filename)

