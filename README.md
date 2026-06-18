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

## Tests:

You can run two existing tests using the python hash seed "123":

- Linux/MacOS:

```
PYTHONHASHSEED=123 python tests/test_hash_24.py
```
- PowerShell:

```
powershell -Command { $env:PYTHONHASHSEED=123; python .\tests\test_hash_24.py }
```

## Considerations:

- Both the siphash lib and this code are pure python implementations, so the speed will not be as good as the native hash implementation.
- do_siphash_24 only accepts strings as inputs for the time being.
- Except if raise_errors is explicitly True, do_siphash_24 will never fail but return None on errors (logging accordingly)

## How it works:
`legacy_hash_utility/legacy_hash.py` is pretty self explanatory. But long story short, we use ctypes to find The SipHash keys in the shared lib "_Py_HashSecret" on the pythonapi.
Once we find that, we convert both keys to hex, then to int, then we create the composit 128bit key from both 64bit keys as little endians.
We use the SipHash24 algorithm to create a hash, the output is a 64 bit unsigned int, we wrap it as a c_int64 to get a signed 64bit int.
