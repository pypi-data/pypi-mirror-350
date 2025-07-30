# epath
Enhanced Path - drop in replacement for Path/PosixPath from pathlib

Supports compression/decompression and signature verification.

Example use:

```
from enhanced_pathlib import Epath
from Cryptodome.PublicKey import RSA
key = RSA.import_key(open('testpublickey.pem').read())
sig = open('testfile.gz.sig', mode="rb").read()
e = epath.EPath('testfile.gz', signed='sha384', compress='gzip', signature=sig, key=key)
e.read_bytes()
```
If the file sig verifies OK it will decompress it and return it in a manner equivalent to Path.read\_bytes()
