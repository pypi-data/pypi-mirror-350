from math import inf, isnan
from random import random

from extratools_core.math import safediv


def test_safediv() -> None:
    assert isnan(safediv(0, 0))

    assert safediv(1, 0) == inf
    assert safediv(-1, 0) == -inf

    a = random()
    # `random` could be 0
    b = random() + 0.01
    assert safediv(a, b) == a / b
