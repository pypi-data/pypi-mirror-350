from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping, Sequence
from itertools import chain, count, repeat
from typing import cast

from toolz.itertoolz import sliding_window

from .dict import invert
from .seq import iter_to_seq
from .typing import Comparable


def iter_to_grams[T](
    data: Iterable[T],
    *,
    n: int,
    pad: T | None = None,
) -> Iterable[Sequence[T]]:
    if pad is not None:
        data = chain(
            repeat(pad, n - 1),
            data,
            repeat(pad, n - 1),
        )

    return sliding_window(n, data)


def is_sorted[T](
    data: Iterable[T],
    *,
    key: Callable[[T], Comparable] | None = None,
    reverse: bool = False,
) -> bool:
    local_key: Callable[[T], Comparable]
    if key is None:
        def default_key(v: T) -> Comparable:
            return cast("Comparable", v)

        local_key = default_key
    else:
        local_key = key

    return all(
        (
            local_key(prev) >= local_key(curr) if reverse
            else local_key(prev) <= local_key(curr)
        )
        for prev, curr in sliding_window(2, data)
    )


def filter_by_positions[T](poss: Iterable[int], data: Iterable[T]) -> Iterable[T]:
    p: Iterator[int] = iter(poss)

    pos: int | None = next(p, None)
    if pos is None:
        return

    for i, v in enumerate(data):
        if i == pos:
            yield v

            pos = next(p, None)
            if pos is None:
                return


def filter_by_others[T](func: Callable[[T, T], bool], data: Iterable[T]) -> Iterable[T]:
    seq: Sequence[T] = iter_to_seq(data)

    filtered_ids: set[int] = set(range(len(seq)))

    for i, x in enumerate(seq):
        remove: bool = False
        for j in filtered_ids:
            if i == j:
                continue

            if not func(x, seq[j]):
                remove = True
                break

        if remove:
            filtered_ids.remove(i)

    for i in filtered_ids:
        yield seq[i]


def remap[KT, VT](
    data: Iterable[KT],
    mapping: MutableMapping[KT, VT],
    *,
    key: Callable[[KT], VT] | None = None,
) -> Iterable[VT]:
    local_key: Callable[[KT], VT]
    if key is None:
        inverted_mapping: Mapping[VT, KT] = invert(mapping)
        c = count(start=0)

        def default_key(_: KT) -> VT:
            while True:
                v: int = next(c)
                if v not in inverted_mapping:
                    return cast("VT", v)

        local_key = default_key
    else:
        local_key = key

    k: KT
    for k in data:
        yield mapping.setdefault(k, local_key(k))
