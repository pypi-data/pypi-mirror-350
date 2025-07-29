from collections.abc import Iterable, Sequence
from itertools import combinations

from toolz import isdistinct

from .itertools import filter_by_others


def candidate_keys[T](
    cols: Sequence[Sequence[T]],
    *,
    max_cols: int = 1,
) -> Iterable[tuple[int, ...]]:
    return map(tuple, filter_by_others(
        # Note that `x > y` (means x is superset of any y) is different from
        # `not x <= y` (means x is not subset of any y)
        lambda x, y: not x <= y,
        map(set, (
            col_ids
            for i in range(1, max_cols + 1)
            for col_ids in combinations(range(len(cols)), i)
            if isdistinct(zip(*[cols[col_id] for col_id in col_ids], strict=True))
        )),
    ))
