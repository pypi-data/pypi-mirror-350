from collections.abc import Callable, Iterable
from io import StringIO
from typing import cast

from toolz import sliding_window

from .typing import Comparable


def sorted_to_str[T](
    seq: Iterable[T],
    *,
    key: Callable[[T], Comparable] | None = None,
) -> str:
    def default_key(v: T) -> Comparable:
        return cast("Comparable", v)

    local_key: Callable[[T], Comparable] = default_key if key is None else key

    s = StringIO()

    first: bool = True
    for prev, curr in sliding_window(2, seq):
        if local_key(prev) > local_key(curr):
            raise ValueError

        if first:
            s.write(repr(prev))
            first = False

        s.write(" == " if local_key(prev) == local_key(curr) else " < ")
        s.write(repr(curr))

    return s.getvalue()
