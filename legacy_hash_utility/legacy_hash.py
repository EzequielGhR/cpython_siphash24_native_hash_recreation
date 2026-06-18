import os
import ctypes
import logging

from typing import Optional
from siphash import SipHash_2_4


logger = logging.getLogger("siphash")
logger.setLevel(logging.INFO)

# We need to recreate the structure of _Py_HashSecret_t in the CPython project
# You can take a look here:
# https://github.com/python/cpython/blob/8646385076ea4f6ef08682d8ef07a544d3b4ef30/Include/internal/pycore_pyhash.h#L42

class SipHashKeys(ctypes.Structure):
    """
    This represents the following structure in C:
    
        #include <stdint.h>
        
        typedef struct {
            uint64_t k0;
            uint64_t k1;
        } SipHashKeys;

    k0 and k1 are the keys we need to create the composit key for the SipHash algorithm.
    """
    _fields_ = [
        ("k0", ctypes.c_uint64),
        ("k1", ctypes.c_uint64),
    ]


class HashSecret(ctypes.Union):
    """
    This represents the following union in C:
    
        typedef Union {
            usigned char uc[24];
            SipHashKeys siphash;
        } HashSecret;

    This is roughly the exported type we need.
    """
    _fields_ = [
        ("uc", ctypes.c_ubyte * 24),
        ("siphash", SipHashKeys),
    ]


def do_siphash_24(src: str, raise_errors = False) -> Optional[str]:
    return _do_hashing(src, raise_errors)


def _do_hashing(src: str, raise_errors = False, algo: Callable = SipHash_2_4):
    """
    This function provides the possiblity of using other hashing algorithms, to recreate different versions
    of the native python hashing. However currently only SipHash_2_4 exists in siphash lib.
    """
    if not isinstance(src, str):
        msg = "Only string hashing is implemented"
        logger.error(msg)
        if raise_errors:
            raise NotImplementedError(msg)
        return None
    
    key = _get_hash_key(raise_errors)
    if key is None:
        return None

    try:
        shash = algo(key, src.encode()).hash()
    except Exception as e:
        logger.error(str(e))
        if raise_errors:
            raise e
        return None

    # shash is by default an unsigned 64 bit int
    # We wrap it as a c_int64 from ctypes to get signed 64 bit int
    return ctypes.c_int64(shash).value


def _get_hash_key(raise_errors = False) -> Optional[bytes]:
    if not os.getenv("PYTHONHASHSEED"):
        msg = "Python hash seed is not set"
        logger.error(msg)
        if raise_errors:
            raise ValueError(msg)
    
    k0: int
    k1: int
    try:
        # _Py_HashSecret shared lib is exposed in the pythonapi on runtime
        secret = HashSecret.in_dll(ctypes.pythonapi, "_Py_HashSecret")
        k0 = int(hex(secret.siphash.k0), 16)
        k1 = int(hex(secret.siphash.k1), 16)
    except Exception as e:
        logger.error(str(e))
        if raise_errors:
            raise e
        return None

    # k0 and k1 need to be converted to 64bit (8 byte) little endians
    return k0.to_bytes(8, "little") + k1.to_bytes(8, "little")
