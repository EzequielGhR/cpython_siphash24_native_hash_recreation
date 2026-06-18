import sys
import os

sys.path.append("./")
from legacy_hash_utility import hash_func_24, do_siphash_24


def test_conditional_import():
    print("Function:", hash_func_24.__name__)
    if sys.hash_info.algorithm == "siphash24":
        assert hash_func_24 is hash
    else:
        assert hash_func_24 is do_siphash_24


def test_do_siphash_24():
    assert os.getenv("PYTHONHASHSEED") == "123", "You need to use 123 as hashseed for this test to make sense"

    source = {
        'random': 3633997531699556129,
        'something': -5651196473118215676,
        '12345678': 7416903422529155814,
        '0098954443': 4646777931369433020,
        '[]][]][l;l;k': 5797920354404337993,
        'zzxeerkks;dldkrjyjgf009-0-908': 6496525991778967080
    }

    for (k, v) in source.items():
        print(f"Checking hash from {k} == {v}")
        assert do_siphash_24(k) == v


if __name__ == "__main__":
    test_conditional_import()
    test_do_siphash_24()
