# cpython_siphash24_native_hash_recreation

Recreate CPython siphash24 hash implementation.

## Requirements:

A single library is required: "siphash=0.0.1". All credits to majek (https://github.com/majek).

## Usage:

No package created yet, so just copy the source legacy_hash_utility to use as a module.
Make sure to install siphash `pip install siphash`

### Import raw hash function:

```
from legacy_hash_utility import do_siphash_24 as hash_func
```

### Import conditionally:

To default to the native implementation of the hash when the algorithm is the same, but using
do_siphash_24 otherwise, just import hash_func_24.

```
from legacy_hash_utility import hash_func_24 as hash_func
```

## Considerations:

- Both the siphash lib and this code are pure python implementations, so the speed will not be as good as the native hash implementation.
- do_siphash_24 only accepts strings as inputs for the time being.
- Except if raise_errors is explicitly True, do_siphash_24 will never fail but return None on errors (logging accordingly)
