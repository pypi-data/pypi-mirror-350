from collections.abc import Callable, Iterable, Sequence
from functools import cache
from itertools import chain, combinations

from . import iter_to_seq


def enumerate_subseqs[T](seq: Iterable[T]) -> Iterable[Sequence[T]]:
    seq = iter_to_seq(seq)
    seq_len: int = len(seq)

    for i in range(seq_len):
        for j in range(i + 1, seq_len + 1 if i > 0 else seq_len):
            yield seq[i:j]


def enumerate_subseqs_with_gaps[T](seq: Iterable[T]) -> Iterable[Sequence[T]]:
    seq = iter_to_seq(seq)

    for i in range(1, len(seq)):
        yield from combinations(seq, i)


def best_subseq[T](
    seq: Iterable[T],
    score_func: Callable[[Iterable[T]], float],
) -> Sequence[T]:
    return max(
        chain([[]], enumerate_subseqs(seq)),
        key=score_func,
    )


def best_subseq_with_gaps[T](
    seq: Iterable[T],
    score_func: Callable[[Iterable[T]], float],
) -> Sequence[T]:
    return max(
        chain([[]], enumerate_subseqs_with_gaps(seq)),
        key=score_func,
    )


def common_subseq[T](a: Iterable[T], b: Iterable[T]) -> Iterable[T]:
    @cache
    # Find the start pos in `a` for longest common subseq aligned from right to left
    # between `a[:alen]` and `b[:blen]`
    def align_rec(alen: int, blen: int) -> int:
        if alen == 0 or blen == 0 or aseq[alen - 1] != bseq[blen - 1]:
            return alen

        return align_rec(alen - 1, blen - 1)

    aseq: Sequence[T] = iter_to_seq(a)
    bseq: Sequence[T] = iter_to_seq(b)

    for k in range(*max(
        (
            (align_rec(i, j), i)
            for i in range(len(aseq) + 1)
            for j in range(len(bseq) + 1)
        ),
        key=lambda x: x[1] - x[0],
    )):
        yield aseq[k]


def is_subseq[T](a: Iterable[T], b: Iterable[T]) -> bool:
    aseq: Sequence[T] = iter_to_seq(a)
    bseq: Sequence[T] = iter_to_seq(b)

    if len(aseq) > len(bseq):
        return False

    return any(
        aseq == bseq[j:j + len(aseq)]
        for j in range(len(bseq) - len(aseq) + 1)
    )


def common_subseq_with_gaps[T](a: Iterable[T], b: Iterable[T]) -> Iterable[T]:
    alignment: tuple[Iterable[T | None], Iterable[T | None]] = align(a, b)

    return (
        x
        for x, y in zip(
            *alignment,
            strict=True,
        )
        if x is not None and y is not None
    )


def is_subseq_with_gaps[T](a: Iterable[T], b: Iterable[T]) -> bool:
    alignment: tuple[Iterable[T | None], Iterable[T | None]] = align(a, b)

    return all(
        y is not None
        for y in alignment[1]
    )


def align[T](
    a: Iterable[T],
    b: Iterable[T],
    *,
    default: T | None = None,
) -> tuple[Iterable[T | None], Iterable[T | None]]:
    def merge(
        prev: tuple[int, tuple[Sequence[T | None], Sequence[T | None]]],
        curr: tuple[T | None, T | None],
    ) -> tuple[int, tuple[Sequence[T | None], Sequence[T | None]]]:
        prev_matches: int
        u: Sequence[T | None]
        v: Sequence[T | None]
        prev_matches, (u, v) = prev

        x: T | None
        y: T | None
        x, y = curr

        return (prev_matches + 1) if x == y else prev_matches, ([*u, x], [*v, y])

    @cache
    def align_rec(alen: int, blen: int) -> tuple[
        int,
        tuple[Sequence[T | None], Sequence[T | None]],
    ]:
        if alen == 0:
            return 0, (
                [default] * blen, bseq[:blen],
            )
        if blen == 0:
            return 0, (
                aseq[:alen], [default] * alen,
            )

        return max(
            (
                merge(align_rec(alen - 1, blen), (aseq[alen - 1], default)),
                merge(align_rec(alen, blen - 1), (default, bseq[blen - 1])),
                merge(align_rec(alen - 1, blen - 1), (aseq[alen - 1], bseq[blen - 1])),
            ),
            key=lambda x: x[0],
        )

    aseq: Sequence[T] = iter_to_seq(a)
    bseq: Sequence[T] = iter_to_seq(b)

    return align_rec(len(aseq), len(bseq))[1]
