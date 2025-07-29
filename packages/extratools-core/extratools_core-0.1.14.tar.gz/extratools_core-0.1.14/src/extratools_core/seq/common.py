from collections.abc import Callable, Iterable, Sequence


def iter_to_seq[T](
    data: Iterable[T],
    target: Callable[[Iterable[T]], Sequence[T]] = tuple,
) -> Sequence[T]:
    if isinstance(data, Sequence):
        return data

    return target(data)
