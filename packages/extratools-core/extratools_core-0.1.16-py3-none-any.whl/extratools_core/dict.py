from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence


def invert[KT, VT](d: Mapping[KT, VT]) -> Mapping[VT, KT]:
    return {
        v: k
        for k, v in d.items()
    }


def invert_safe[KT, VT](d: Mapping[KT, VT]) -> Mapping[VT, Sequence[KT]]:
    r: defaultdict[VT, list[KT]] = defaultdict(list)

    for k, v in d.items():
        r[v].append(k)

    return r


def inverted_index[T](
    seqs: Iterable[Sequence[T]],
) -> Mapping[T, Sequence[tuple[int, Sequence[int]]]]:
    index: defaultdict[T, list[tuple[int, list[int]]]] = defaultdict(list)

    for i, seq in enumerate(seqs):
        seq_index: defaultdict[T, list[int]] = defaultdict(list)
        for j, item in enumerate(seq):
            seq_index[item].append(j)

        for item, poss in seq_index.items():
            index[item].append((i, poss))

    return index
