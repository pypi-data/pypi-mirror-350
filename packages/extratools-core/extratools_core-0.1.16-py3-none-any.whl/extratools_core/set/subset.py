from collections.abc import Callable, Iterable
from collections.abc import Set as AbstractSet

from ..seq.subseq import best_subseq_with_gaps, enumerate_subseqs_with_gaps


def enumerate_subsets[T](a: AbstractSet[T]) -> Iterable[AbstractSet[T]]:
    return map(frozenset, enumerate_subseqs_with_gaps(a))


def best_subset[T](
    a: set[T],
    score_func: Callable[[Iterable[T]], float],
) -> set[T]:
    return set(best_subseq_with_gaps(tuple(a), score_func))


def set_cover[T](
    whole: Iterable[T],
    covers: Iterable[AbstractSet[T]],
    *,
    score_func: Callable[[AbstractSet[T]], float] | None = None,
) -> Iterable[AbstractSet[T]]:
    local_score_func: Callable[[AbstractSet[T]], float] = score_func or len

    whole_set: set[T] = set(whole)
    cover_sets: set[frozenset[T]] = {frozenset(x) for x in covers}

    while whole_set and cover_sets:
        best_score: float | None
        best_set: frozenset[T] | None
        best_score, best_set = None, None

        for curr in cover_sets:
            temp_set: frozenset[T] = curr & whole_set
            if temp_set:
                temp_score: float = local_score_func(temp_set)
                if not best_score or temp_score > best_score:
                    best_score, best_set = temp_score, curr

        if not best_set:
            return

        yield best_set

        whole_set.difference_update(best_set)
        cover_sets.remove(best_set)
