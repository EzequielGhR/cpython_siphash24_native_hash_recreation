import sys

from typing import Callable
from .legacy_hash import do_siphash_24
from .legacy_hash import logger


__all__ = [
    "hash_func_24",
    "do_siphash_24"
]


hash_func_24: Callable
if sys.hash_info.algorithm == "siphash24":
    logger.warning("Already running a version of python with siphash 24")
    hash_func_24 = hash
else:
    logger.info("Setting hash_function_24 to %s", do_siphash_24.__name__)
    hash_func_24 = do_siphash_24
