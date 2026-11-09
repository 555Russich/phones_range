"""Smallest check that number-generation + filtering stay correct.

Run: python test_gen.py
"""
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from gen_dict import create_filtered_dict, create_dict

DATA = {
    "900": [{"Регион РФ": "Р1", "Оператор": "OpA", "Диапазон номеров": [[0, 4]], "Кол-во номеров": 5}],
    "916": [{"Регион РФ": "Москва", "Оператор": "МТС", "Диапазон номеров": [[500000, 500002]], "Кол-во номеров": 3}],
}


def args(code=(), region=(), operator=()):
    return Namespace(code=list(code), region=list(region), operator=list(operator))


def gen(a):
    with TemporaryDirectory() as d:
        p = Path(d) / "out.dict"
        create_dict(create_filtered_dict(DATA, a), p)
        return p.read_text().split()


# no filters -> every number; short range must zero-pad (regression guard: the
# old '{:<07d}' bug turned 0500000 into 5000000 -> 9165000000).
allnums = gen(args())
assert "9160500000" in allnums and "9165000000" not in allnums, allnums
assert sorted(allnums) == ["9000000000", "9000000001", "9000000002", "9000000003",
                           "9000000004", "9160500000", "9160500001", "9160500002"], allnums

# AND across filter types, OR within a list
assert gen(args(operator=["МТС"])) == ["9160500000", "9160500001", "9160500002"]
assert gen(args(code=["900"], operator=["МТС"])) == []  # don't co-occur -> empty

print("ok")
