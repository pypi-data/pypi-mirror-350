import operator
from collections import Counter
from collections.abc import Callable, Iterable, Iterator, Mapping
from itertools import groupby, repeat
from typing import Any, cast

from toolz import itertoolz, unique

from ..typing import Comparable
from .common import iter_to_seq  # noqa: F401


def sorted_by_rank[T](
    data: Iterable[T],
    ranks: Iterable[Comparable],
    *,
    _reverse: bool = False,
) -> list[T]:
    return [
        v
        for v, _ in sorted(
            zip(data, ranks, strict=True),
            key=lambda x: x[1],
            reverse=_reverse,
        )
    ]


def compress[T](
    data: Iterable[T],
    key: Callable[[T], Any] | None = None,
) -> Iterable[tuple[T, int]]:
    for k, g in groupby(data, key=key):
        yield (k, itertoolz.count(g))


def decompress[T](data: Iterable[tuple[T, int]]) -> Iterable[T]:
    for k, n in data:
        yield from repeat(k, n)


def to_deltas[T](
    data: Iterable[T],
    op: Callable[[T, T], T] = operator.sub,
) -> Iterable[T]:
    seq: Iterator[T] = iter(data)

    curr: T | None = next(seq, None)
    if curr is None:
        return

    yield curr

    prev: T = curr
    for curr in seq:
        yield op(curr, prev)

        prev = curr


def from_deltas[T](
    data: Iterable[T],
    op: Callable[[T, T], T] = operator.add,
) -> Iterable[T]:
    seq: Iterator[T] = iter(data)

    curr: T | None = next(seq, None)
    if curr is None:
        return

    yield curr

    prev: T = curr
    for curr in seq:
        res: T = op(prev, curr)
        yield res

        prev = res


def key_frequencies[KT, VT](
    *seqs: Iterable[KT],
    key: Callable[[KT], VT] | None = None,
) -> Mapping[VT, int]:
    c: Counter[VT] = Counter()
    for seq in seqs:
        c.update(cast("Iterable[VT]", unique(seq, key=key)))

    return c
