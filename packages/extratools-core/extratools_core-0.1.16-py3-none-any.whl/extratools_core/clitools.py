from collections.abc import Iterable
from io import StringIO
from itertools import zip_longest

from wcwidth import wcswidth


def alignment_to_str[T](
    *seqs: Iterable[T | None],
    default: str = "",
    separator: str = " | ",
) -> str:
    """
    Example:
    ``` python
    In [1]: from extratools_core.cli import alignment_to_str

    In [2]: print(alignment_to_str(["吃饭", "喝水", "看电视"], ["Ada", "Bob", "Chad"]))
    '吃饭' | '喝水' | '看电视'
    'Ada'  | 'Bob'  | 'Chad'
    ```
    """

    strs: list[StringIO] = []

    for i, col in enumerate(zip_longest(*seqs, fillvalue=default)):
        if i == 0:
            strs = [StringIO() for _ in col]
        else:
            for s in strs:
                s.write(separator)

        vals: list[str] = [
            default if v is None else repr(v)
            for v in col
        ]
        max_width: int = max(
            wcswidth(val)
            for val in vals
        )
        pads: list[str] = [
            (max_width - wcswidth(val)) * ' '
            for val in vals
        ]

        for s, pad, val in zip(strs, pads, vals, strict=True):
            s.write(val)
            s.write(pad)

    return '\n'.join([s.getvalue() for s in strs])
